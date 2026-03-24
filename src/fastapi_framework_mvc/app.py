#!/usr/bin/python3
# coding: utf-8


__author__ = 'Frederick NEY'

import logging
import os

import fastapi_framework_mvc.core as core
from fastapi_framework_mvc.cli import parser as cli
from fastapi_framework_mvc.common import BaseApp
from fastapi_framework_mvc.config import Environment
from fastapi_framework_mvc.core.logging import configure_basic_logger
from fastapi_framework_mvc.utils import make_controller, make_middleware, make_project

logging.info("Starting server...")
if "CONFIG_FILE" not in os.environ and not os.path.exists("/etc/fastapi/"):
    os.environ.setdefault(
        'CONFIG_FILE',
        "config/config.yml" if os.path.exists("config/config.yml")
        else "/etc/fastapi/config.yml" if os.path.exists("/etc/fastapi/config.yml")
        else None
    )
if not 'CONFIG_FILE' in os.environ:
    print('Unable tp detect any configuration files, use CONFIG_FILE env to override detection')
    exit(255)
logging.info("Loading configuration file...")
Environment.load(os.environ['CONFIG_FILE'])
logging.info("Configuration file loaded...")
try:
    loglevel = Environment.SERVER['LOG']['LEVEL']
    configure_basic_logger(loglevel)
except KeyError as e:
    configure_basic_logger(logging.INFO)
base_app = BaseApp()
base_app.load_app()
core.Process.init(tracking_mode=False)
logging.info("Server is now starting...")
app = core.Process.get()

if __name__ == '__main__':
    cli()
