#!/usr/bin/python3
# coding: utf-8


__author__ = 'Frederick NEY'

import logging
import os

import fastapi_framework_mvc.Server as Server
from fastapi_framework_mvc.Config import Environment
from fastapi_framework_mvc.Database import Database
from fastapi_framework_mvc.Utils import make_controller, make_middleware, make_project


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
logging.info("Loading configuration file...")
Environment.load(os.environ.get('CONFIG_FILE', "/etc/server/config.json"))
try:
    loglevel = Environment.SERVER['LOG']['LEVEL']
    logging.basicConfig(
        level=loglevel.upper(),
        format='%(asctime)s %(levelname)s %(message)s'
    )
except KeyError as e:
    logging.basicConfig(
        level=logging.getLevelName(logging.INFO),
        format='%(asctime)s %(levelname)s %(message)s'
    )
logging.debug("Connecting to default database...")
Database.register_engines(echo=Environment.SERVER['CAPTURE'])
Database.init()
logging.debug("Default database connected...")
Server.Process.init(tracking_mode=False)
# Server.Process.init_sheduler()
logging.debug("Server initialized...")
Server.Process.load_plugins()
logging.debug("Loading server routes...")
Server.Process.load_routes()
Server.Process.load_middleware()
logging.debug("Server routes loaded...")
logging.debug("Loading websocket events")
Server.Process.load_socket_events()
logging.debug("Websocket events loaded...")
# app.teardown_appcontext(Database.save)
logging.info("Server is now starting...")
app = Server.Process.get()

if __name__ == '__main__':
    parser()
    app.run(host=Environment.SERVER['BIND']['ADDRESS'], port=Environment.SERVER['BIND']['PORT'])
