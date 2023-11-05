import argparse
import http
import logging
import sys
from pathlib import Path

from .types import LeagueType
from .utils import EnumAction


DEFAULT_DATA_FILES = [f'data-{lt.value}.json' for lt in LeagueType]

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(prog=__package__)
subparsers = parser.add_subparsers(dest='command')

gen = subparsers.add_parser('gen')
gen.add_argument(
    'league_type',
    type=LeagueType,
    action=EnumAction,
)

pub = subparsers.add_parser('pub')
pub.add_argument(
    'filename',
    nargs='+',
    default=DEFAULT_DATA_FILES,
    choices=DEFAULT_DATA_FILES,
)

args = parser.parse_args()

#
# python -m data gen
#
if args.command == 'gen':
    import datetime
    import itertools
    import json
    import pathlib
    from dataclasses import asdict

    from .beasts import get_beasts
    from .leagues import get_leagues
    from .tft import get_tft_channels
    from .tools import get_tools
    from .wiki import get_items

    league = get_leagues()[args.league_type]
    print(f'Aggregating data for {league.title} ({league.slug})...')

    data = []

    for num, entry in enumerate(
        itertools.chain(
            get_items(league),
            get_beasts(league),
            get_tools(league),
            get_tft_channels(args.league_type),
        ),
    ):
        data.append({'id': num, **asdict(entry)})

    now = datetime.datetime.now(tz=datetime.UTC)
    doc = {
        'meta': {
            'league': args.league_type.value,
            'timestamp': datetime.datetime.timestamp(now),
            'timestamp_human': now.isoformat(),
        },
        'data': data,
    }

    with pathlib.Path(f'data-{args.league_type.value}.json').open('w') as file:
        json.dump(doc, file)


#
# python -m data pub
#
elif args.command == 'pub':
    import os
    import time

    import boto3
    import humanize
    from botocore.exceptions import ClientError

    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
        aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
    )

    uploaded = []
    for filename in args.filename:
        size = humanize.naturalsize(Path.stat(filename).st_size, binary=True)
        print(f'Uploading {filename} ({size}) to S3...', end='')
        try:
            s3.upload_file(
                filename,
                os.environ['S3_PUBLIC_BUCKET'],
                filename,
                ExtraArgs={'ContentType': 'application/json'},
            )
        except ClientError as ex:
            print(f'\nFailed to upload {filename}: {ex}')
        else:
            uploaded.append(filename)
            print(' Done.')

    if items := [f'/{filename}' for filename in uploaded]:
        print('Invalidating CloudFront cache for the following files:')
        for item in items:
            print(f' * {item}')

        cloudfront = boto3.client(
            'cloudfront',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
            aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
        )

        response = cloudfront.create_invalidation(
            DistributionId=os.environ['CLOUDFRONT_DISTRIBUTION_ID'],
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(items),
                    'Items': items,
                },
                'CallerReference': str(time.time()),
            },
        )
        response_status = response['ResponseMetadata']['HTTPStatusCode']
        assert response_status == http.HTTPStatus.CREATED, f'Invalidation failed with status {response_status}.'
    else:
        print('No files to invalidate in CloudFront.')


else:
    parser.print_help()
    sys.exit(1)
