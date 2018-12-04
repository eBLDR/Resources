# -*- coding: utf-8 -*-
import importlib

from main import ENVIRONMENT

CONFIG_PATH = 'main.config'

try:
    settings = importlib.import_module('.%s' % ENVIRONMENT, CONFIG_PATH)
except ImportError as e:
    raise RuntimeError('Unable to import config module {}'.format(ENVIRONMENT))

