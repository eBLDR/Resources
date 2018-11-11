"""
- By eBLDR -

Setting manager based on environment.

One module for each env should exist - env_name.py
"""
import os


def get_environment():
    """
    Get the current application environment based on environment
    variable or hostname. Returns 'local' by default.
    """
    os_env = os.environ.get('ENVIRONMENT', '')

    if os_env.lower() == 'production':
        env = 'production'
    elif os_env.lower() == 'development':
        env = 'development'
    else:
        env = 'local'

    return env


ENVIRONMENT = get_environment()

#####

import importlib

# Replace me
CONFIG_PATH = '.'

try:
    settings = importlib.import_module('.%s' % ENVIRONMENT, CONFIG_PATH)
except ImportError as e:
    raise RuntimeError('Unable to import config module {}'.format(ENVIRONMENT))
