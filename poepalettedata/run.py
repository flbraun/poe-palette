import dataclasses
import datetime
import itertools
import json
import logging
import time

import boto3
import humanize

from poepalettedata.beasts import get_beasts
from poepalettedata.tft import get_tft_channels
from poepalettedata.tools import get_tools
from poepalettedata.utils import Config, get_secret
from poepalettedata.wiki import get_items


logger = logging.getLogger(__name__)


def generate(config: Config) -> None:
    logger.info('Aggregating data for %(league_type)s', {'league_type': config.league_type})

    data = []

    for num, entry in enumerate(
        itertools.chain(
            get_items(config),
            get_beasts(config),
            get_tools(config),
            get_tft_channels(config),
        ),
    ):
        data.append({'id': num, **dataclasses.asdict(entry)})

    now = datetime.datetime.now(tz=datetime.UTC)
    doc = {
        'meta': {
            'league': config.league_type,
            'timestamp': datetime.datetime.timestamp(now),
            'timestamp_human': now.isoformat(),
        },
        'data': data,
    }

    with config.data_file.open('w', encoding='utf-8') as file:
        json.dump(doc, file)

    logger.info('Data written to %(filename)r', {'filename': config.data_file})


def upload(config: Config) -> None:
    size = humanize.naturalsize(config.data_file.stat().st_size, binary=True)
    logger.info('Uploading %(filename)r (%(size)s) to S3', {'filename': config.data_file, 'size': size})

    s3 = boto3.client('s3')
    s3.upload_file(
        str(config.data_file),
        get_secret('S3_BUCKET_NAME'),
        config.data_file.name,
        ExtraArgs={'ContentType': 'application/json'},
    )

    logger.info('Upload complete.')


def publish(config: Config) -> None:
    logger.info('Invalidating CloudFront cache for the uploaded file.')

    cloudfront = boto3.client('cloudfront')
    cloudfront.create_invalidation(
        DistributionId=get_secret('CLOUDFRONT_DISTRIBUTION_ID'),
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': [f'/{config.data_file.name}'],
            },
            'CallerReference': str(time.time()),
        },
    )

    logger.info('Invalidation created.')


def run(config: Config) -> None:
    logger.info('Running with %(config)r', {'config': config})

    generate(config)

    if config.upload:
        upload(config)

    if config.publish:
        publish(config)
