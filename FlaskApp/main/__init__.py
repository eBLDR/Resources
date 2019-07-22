# -*- coding: utf8 -*-
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
