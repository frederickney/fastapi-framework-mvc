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

try:
    import gunicorn.app.base
except ImportError:
    print(
        f"{__package__}.{os.path.basename(__file__).replace('.py', '')} is not compatible with windows, use {__package__}.{os.path.basename(__file__).replace('wsgi.py', 'server')} or {__package__}.{os.path.basename(__file__).replace('wsgi', 'asgi')} instead.")
    exit(0)
from fastapi_framework_mvc.config import Environment
from fastapi_framework_mvc.core.logging import setup_file_logging, configure_basic_logger
from fastapi_framework_mvc.common import Logging
from fastapi_framework_mvc.common import BaseApp
from fastapi_framework_mvc.core.process import number_of_workers
from six import iteritems

parser = argparse.ArgumentParser(description='Python FLASK USGI server')
parser.add_argument(
    '-d', '--disable-log-files',
    action='store_true',
    required=False,
    help='Deactivate logs to file'
)


class Server(gunicorn.app.base.Application, BaseApp):

    def init(self, parser, opts, args):
        """
        Used to print options on dev not for production
        """
        print(parser)
        print(opts)
        print(args)

    def __init__(self, options=None):
        """
        Initialize the server using gunicorn
        """
        Server.options = (options or {}) if not hasattr(Server, 'options') else Server.options
        super(Server, self).__init__()
        BaseApp.__init__(self)
        self.application = Server.application()

    def reload(self):
        """
        reload app function.
        Called on gunicorn.reload event
        :return:
        """
        logging.info('reloading')
        try:
            import gevent.monkey
            gevent.monkey.patch_all()
        except ImportError as e:
            pass
        Environment.reload(os.environ['CONFIG_FILE'])
        self.application = Server.application()
        Server.load_options()
        super(Server, self).reload()

    def load_config(self):
        """
        Load gunicorn options
        """
        logging.info(Server.options)
        config = dict([(key, value) for key, value in iteritems(Server.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        """
        Load app for gunicorn.

        Called on gunicorn.load event
        """
        try:
            import eventlet
            eventlet.monkey_patch(all=True)
        except ImportError as e:
            pass
        try:
            import eventlet
            eventlet.monkey_patch(all=True)
        except ImportError as e:
            pass
        return self.application

    @classmethod
    def load_options(cls):
        """
        Sets gunicorn options
        """
        cls.options = {
            'bind': '%s:%i' % (Environment.SERVER['BIND']['ADDRESS'], int(Environment.SERVER['BIND']['PORT'])),
            'workers': number_of_workers(),
            'threads': Environment.SERVER['THREADS_PER_CORE'],
            'capture_output': Environment.SERVER['CAPTURE'],
            "loglevel": Logging.get_loglevel(),
            "worker_class": Environment.SERVER['WORKERS'],
            "reload_engine": 'poll'
        }
        if Logging.logging_dir_exist:
            cls.options["errorlog"] = os.path.join(os.environ.get("log_dir"), 'fastapi-error.log')
            cls.options["accesslog"] = os.path.join(os.environ.get("log_dir"), 'fastapi-access.log')
        if 'SSL' in Environment.SERVER:
            cls.options["certfile"] = Environment.SERVER['SSL']['Certificate']
            cls.options["keyfile"] = Environment.SERVER['SSL']['PrivateKey']


def start(args: argparse.ArgumentParser):
    """
    Loads options and starts process.
    """
    logging.info("Loading options...")
    Server.load_options()
    logging.info("Options loaded...")
    logging.info("Starting the server...")
    try:
        Server().run()
    except RuntimeError as e:
        exit(255)


def main():
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
    if "CONFIG_FILE" not in os.environ and not os.path.exists("/etc/fastapi/"):
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
    start(args)


if __name__ == '__main__':
    main()
