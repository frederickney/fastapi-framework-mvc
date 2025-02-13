# coding: utf-8


__author__ = 'Frederick NEY'

import functools
import warnings
from datetime import datetime, timedelta

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from . import WS, Web, ErrorHandler, Middleware, Socket, Plugins


def configure_logs(name, format, output_file, debug='info'):
    """

    :param name:
    :type name: str
    :param format:
    :type format: str
    :param output_file:
    :type output_file: str
    :param debug:
    :type debug: str
    :return:
    """
    import logging
    logger = logging.getLogger(name)
    formatter = logging.Formatter(format)
    file_handler = logging.FileHandler(output_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logging.getLevelName(debug.upper())
    logger.setLevel(logging.getLevelName(debug.upper()))


class Process(object):
    _app: FastAPI = None
    _pidfile = "/run/fastapi.pid"
    _login_manager = None
    _csrf = None
    temlates = None
    sso = None
    openid = None
    ldap = None
    saml = None

    @classmethod
    def init(cls, tracking_mode=False):
        """

        :param tracking_mode:
        :type tracking_mode: bool
        :return:
        :rtype: fastapi.FastAPI
        """
        import os.path
        import pathlib
        from fastapi import FastAPI
        from fastapi_framework_mvc.Config import Environment
        cls._app = FastAPI()
        if 'STATIC_PATH' in Environment.SERVER:
            cls._load_statics()
        if 'TEMPLATE_PATH' in Environment.SERVER:
            cls._load_templates()
        if 'CONFIG' in Environment.FASTAPI:
            if Environment.FASTAPI['CONFIG'] is not None:
                cls._app.extra.update(Environment.FASTAPI['CONFIG'])
            if 'OpenID' in Environment.Logins:
                from fastapi_login_oidc import OIDC
                cls.openid = OIDC(prefix='OpenID')
                cls.openid.init_app(cls._app)
            if 'SAML2' in Environment.Logins:
                from fastapi_login_saml.client import SAML
                cls.saml = SAML(prefix='SAML2')
                cls.saml.init_app(cls._app)
        return cls._app

    @classmethod
    def _load_statics(cls):
        cls._app.mount(
            '/statics' if 'STATIC_URL' not in Environment.SERVER else Environment.SERVER['STATIC_URL'],
            StaticFiles(directory=Environment.SERVER['STATIC_PATH']), 
            name="static"
        )
    
    @classmethod
    def _load_templates(cls):
        cls.templates = Jinja2Templates(directory=Environment.SERVER['TEMPLATE_PATH'])

    @classmethod
    def instanciate(cls):
        """
            :return:
            :rtype: fastapi.FastAPI
        """
        return cls._app

    @classmethod
    def start(cls, args):
        """

        :param args:
        :return:
        """
        cls._args = args
        import uvicorn
        from fastapi_framework_mvc.Config import Environment
        if args.listening_address is not None:
            # logger.info("Starting listening on " + args.listening_address + " on port " + args.listening_port)
            print("Starting listening on %s on port %d" % (args.listening_address, int(args.listening_port)))
            if 'SSL' in Environment.SERVER:
                try:
                    if args.pid:
                        cls.pid()
                    uvicorn.run(
                        cls._app,
                        host=args.listening_address, 
                        port=int(args.listening_port),
                        ssl_keyfile=Environment.SERVER['SSL']['PrivateKey'],
                        ssl_certfile=Environment.SERVER['SSL']['Certificate']
                    )
                finally:
                    if args.pid:
                        cls.shutdown()
            else:
                try:
                    if args.pid:
                        cls.pid()
                    uvicorn.run(
                        cls._app,
                        host=args.listening_address, 
                        port=int(args.listening_port),
                    )
                finally:
                    if args.pid:
                        cls.shutdown()
        else:
            # logger.info("Starting listening on 0.0.0.0 on port " + args.listening_port)
            print("Starting listening on 0.0.0.0 on port %d" % int(args.listening_port))
            if 'SSL' in Environment.SERVER:
                try:
                    if args.pid:
                        cls.pid()
                    uvicorn.run(
                        cls._app,
                        host="0.0.0.0", 
                        port=int(args.listening_port),
                        ssl_keyfile=Environment.SERVER['SSL']['PrivateKey'],
                        ssl_certfile=Environment.SERVER['SSL']['Certificate']
                    )
                finally:
                    if args.pid:
                        cls.shutdown()
            else:
                try:
                    if args.pid:
                        cls.pid()
                    uvicorn.run(
                        cls._app,
                        host="0.0.0.0", 
                        port=int(args.listening_port),
                    )
                finally:
                    if args.pid:
                        cls.shutdown()
            # logger.info("Server is running")

    @classmethod
    def wsgi_setup(cls):
        """

        :return:
        :rtype: fastapi.FastAPI
        """
        return cls._app


    @classmethod
    def load_plugins(cls):
        Plugins.Load(
            server=cls._app,
        )

    @classmethod
    def load_routes(cls):
        """

        :return:
        """
        WS.Route(cls._app)
        Web.Route(cls._app)
        ErrorHandler.Route(cls._app)

    @classmethod
    def load_middleware(cls):
        """

        :return:
        """
        Middleware.Load(cls._app)

    @classmethod
    def load_socket_events(cls):
        """

        :return:
        """
        Socket.Load(cls._app)

    @classmethod
    def pid(cls):
        """

        :return:
        """
        import os
        import sys
        pid = str(os.getpid())
        if os.path.isfile(cls._pidfile):
            print("%s already exists, exiting" % cls._pidfile)
            sys.exit()
        pid_file = open(cls._pidfile, 'w')
        pid_file.write(pid)
        pid_file.close()

    @classmethod
    def shutdown(cls):
        """

        :return:
        """
        import os
        os.unlink(cls._pidfile)

    @classmethod
    def get(cls):
        """

        :return:
        :rtype: fastapi.FastAPI
        """
        return cls._app

    @classmethod
    def stop(cls, code=0):
        """

        :param code:
        :type: int
        :return:
        """
        if cls._args.pid:
            cls.shutdown()
        exit(code)

    @classmethod
    def login_manager(cls, login_manager=None):
        """

        :param login_manager:
        :type login_manager: fastapi_login.LoginManager
        :return:
        :rtype: fastapi_login.LoginManager
        """
        if login_manager:
            try:
                from fastapi_login import LoginManager
                if (
                        not callable(login_manager)
                        and isinstance(login_manager, object)
                        and type(login_manager) is LoginManager
                ):
                    cls._login_manager = login_manager
            except ImportError:
                pass
        return cls._login_manager


