# -*- coding: utf8 -*-
from flask import Flask, session

from main.config import settings

APP = Flask(__name__, template_folder=settings.APP_TEMPLATES_FOLDER)

APP.secret_key = settings.APP_SECRET_KEY

from main.app import app_controller
