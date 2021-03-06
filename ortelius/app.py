import os
import hug

from ortelius.api import Dicts, Elements, Shapes
from ortelius import settings

try:
    env = os.environ['APP_SETTINGS']
except Exception:
    env = os.environ['APP_SETTINGS'] = 'development'

if env == 'testing':
    config = settings.TestingConfig
elif env == 'production':
    config = settings.ProductionConfig
elif env == 'staging':
    config = settings.StagingConfig
else:
    config = settings.DevelopmentConfig


@hug.get('/')
def welcome():
    return 'Welcome to ortelius version {0}'.format(config.API_VERSION)


@hug.extend_api('/elements')
def get_elements():
    return [Elements]


@hug.extend_api('/dicts')
def get_dicts():
    return [Dicts]


@hug.extend_api('/shapes')
def get_shapes():
    return [Shapes]


if __name__ == '__main__':
    welcome.interface.cli()
