#!/usr/bin/python3
# coding: utf-8


__author__ = 'Frederick NEY'

try:
    import gevent.monkey

    gevent.monkey.patch_all()
except ImportError as e:
    pass
try:
    import eventlet

    eventlet.monkey_patch(all=True)
except ImportError as e:
    pass

import argparse
import logging
import os
import sys

from fastapi_framework_mvc.common import BaseApp
from fastapi_framework_mvc.common import Logging
from fastapi_framework_mvc.config import Environment
from fastapi_framework_mvc.core import Process
from fastapi_framework_mvc.core.logging import setup_file_logging, configure_basic_logger
from fastapi_framework_mvc.core.process import number_of_workers

parser = argparse.ArgumentParser(description='Python FLASK USGI server')
parser.add_argument(
    '-d', '--disable-log-files',
    action='store_true',
    required=False,
    help='Deactivate logs to file'
)
parser.add_argument(
    '-a', '--listening-address',
    required=False,
    default=None,
    help='Listening address'
)
parser.add_argument(
    '-p', '--listening-port',
    required=False,
    default=None,
    help='Listening port'
)
parser.add_argument(
    '--pid',
    action='store_true',
    default=False,
    help='Create pid file'
)


class Server(BaseApp):

    def __init__(self, options=None):
        """
        Initialize the server using gunicorn
        """
        Server.options = (options or {}) if not hasattr(Server, 'options') else Server.options
        super(Server, self).__init__()
        self.application = Server.application()

    def load(self):
        """
        Load app for gunicorn.

        Called on gunicorn.load event
        """
        return self.application


def start(args: argparse.ArgumentParser):
    """
    Starts process.
    """
    logging.info("Starting the server...")
    try:
        Process.asgi(f"{__package__}.{os.path.basename(__file__).replace('.py', '')}:process", args)
    except RuntimeError as e:
        exit(255)


""""
main entrypoint for fastapi_framework_mvc.wsgi
loads environments and setups loging handler
"""
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
args = parser.parse_args()
configure_basic_logger(None)
if not args.disable_log_files:
    setup_file_logging()
if "CONFIG_FILE" not in os.environ or not os.path.exists("/etc/fastapi/"):
    os.environ.setdefault(
        'CONFIG_FILE',
        "config/config.yml" if os.path.exists("config/config.yml")
        else "/etc/fastapi/config.yml" if os.path.exists("/etc/fastapi/config.yml")
        else None
    )
if not 'CONFIG_FILE' in os.environ:
    print('Unable tp detect any configuration files, use CONFIG_FILE env to overide detection')
    exit(255)
logging.info("Loading configuration file...")
Environment.load(os.environ['CONFIG_FILE'])
logging.info("Configuration file loaded...")
if not args.listening_address:
    args.listening_address = Environment.SERVER['BIND']['ADDRESS']
if not args.listening_port:
    args.listening_port = Environment.SERVER['BIND']['PORT']
try:
    Logging.set_loglevel(Environment.SERVER['LOG']['LEVEL'])
    configure_basic_logger(level=Environment.SERVER['LOG']['LEVEL'])
except KeyError as e:
    logging.error(e)
    pass
Logging.logging_dir_exist = False
try:
    if not args.disable_log_files:
        os.environ.setdefault('LOG_DIR', Environment.SERVER['LOG']['DIR'])
        setup_file_logging(level=Environment.SERVER['LOG']['LEVEL'])
    logging.info('Logging handler initialized')
except KeyError as e:
    pass
except FileNotFoundError as e:
    pass
except PermissionError as e:
    pass

server = Server()
process = Process.wsgi_setup()

if __name__ == '__main__':
    start(args)
