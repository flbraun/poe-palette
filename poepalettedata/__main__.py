import argparse
import dataclasses
import logging
import pathlib
import tomllib

import sentry_sdk

from poepalettedata.run import run
from poepalettedata.utils import Config, get_secret


# bootstraping
logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s', level=logging.INFO)
if dsn := get_secret('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=dsn,
        environment='prod',
        enable_tracing=True,
    )

# parse from CLi which league type to create data for
parser = argparse.ArgumentParser(__package__)
parser.add_argument('league_type', choices=['challenge', 'challengehc', 'standard', 'hardcore'])
parsed = parser.parse_args()

sentry_sdk.set_tag('config.league_type', parsed.league_type)  # set early in case config parsing crashes
logger = logging.getLogger(__name__)
logger.info('Invoked for league type %(league_type)r', {'league_type': parsed.league_type})

# parse appropriate config file
leagues_file = pathlib.Path(__file__).parent / 'leagues.toml'
leagues_data = leagues_file.read_text()
leagues_conf = tomllib.loads(leagues_data)
config = Config(parsed.league_type, **leagues_conf[parsed.league_type])

# set tags for sentry
sentry_sdk.set_tags({f'config.{k}': v for k, v in dataclasses.asdict(config).items()})

# actual run
run(config)
