#!/usr/bin/python3
# coding: utf-8


__author__ = 'Frederick NEY'

import logging
import os

import fastapi_framework_mvc.core as core
from fastapi_framework_mvc.common import BaseApp
from fastapi_framework_mvc.config import Environment
from fastapi_framework_mvc.core.logging import configure_basic_logger
from fastapi_framework_mvc.utils import make_controller, make_middleware, make_project


def parser():
    import argparse
    parser = argparse.ArgumentParser(description='Python FastAPI server')
    parser.add_argument(
        '-cp', '--create-project',
        help='Create project\nexample:\npython -m fastapi_framework_mvc.cli --create-project webapp',
        required=False
    )
    parser.add_argument(
        '-cc', '--create-controller',
        help='Create controller\nexample:\npython -m fastapi_framework_mvc.cli --create-controller controllers/web/login',
        required=False
    )
    parser.add_argument(
        '-cm', '--create-middleware',
        help='Create middleware\nexample:\npython -m fastapi_framework_mvc.cli --create-middleware test',
        required=False
    )
    args = parser.parse_args()
    if args.create_project:
        make_project(os.getcwd(), args.create_project, os.path.dirname(os.path.realpath(__file__)))
        exit(0)
    elif args.create_controller:
        make_controller(os.getcwd(), args.create_controller)
        exit(0)
    elif args.create_middleware:
        make_middleware(os.getcwd(), args.create_middleware)
        exit(0)


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
app = base_app.application()
core.Process.init(tracking_mode=False)
logging.info("Server is now starting...")
app = core.Process.get()

if __name__ == '__main__':
    parser()
