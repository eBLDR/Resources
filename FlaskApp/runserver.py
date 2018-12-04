#! /usr/bin/python3
#! -*- coding: utf8 -*-
"""
- By eBLDR -

Flask App structure.
"""

from main.config import settings
from main.app import APP

if __name__ == '__main__':
    APP.run(host=settings.APP_HOST, port=settings.APP_PORT)

