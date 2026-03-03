# coding: utf-8


__author__ = 'Frederick NEY'

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi_framework_mvc.config import Environment
from fastapi_framework_mvc.deprecation import outdated
from . import errors
from . import middleware
from . import plugins
from . import socket
from . import web
from . import ws


class Process(object):
    """
    Core class ot the framework, handles all fastapi configuration / registration

    Contains following attributes:
    Attributes
    ----------
        templates: Jinja2Templates
            For templates handling in fastapi.APIRouter.route decorator, server.add_route method or
            fastapi.APIRouter.route decorator
        openid: FastAPIOIDC
            for handling user authentication both in swagger and endpoints uses fastapi_oidc.FastAPIOIDC
        _login_manager:
            deprecated
        _csrf:
            deprecated
        sso:
            deprecated
        ldap:
            deprecated
        saml:
            deprecated
    """

    _app: FastAPI = None
    _pidfile = "/run/fastapi.pid"
    _login_manager = None
    _csrf = None
    templates = None
    sso = None
    openid = None
    ldap = None
    saml = None

    @classmethod
    def init(cls, tracking_mode=False):
        """
        Initialise the framework and creates fastapi instances with others plugins based on configuration
        :param tracking_mode:
        :type tracking_mode: bool
        :return:
        :rtype: fastapi.FastAPI
        """
        import os.path
        import pathlib
        from fastapi import FastAPI
        cls._app = FastAPI()
        Environment.SERVER.setdefault(
            'STATIC_PATH',
            os.path.join(pathlib.Path(__file__).resolve().parent.resolve().parent, 'static')
        )
        Environment.SERVER.setdefault(
            'TEMPLATE_PATH',
            os.path.join(pathlib.Path(__file__).resolve().parent.resolve().parent, 'templates')
        )
        cls._load_statics()
        cls._load_templates()
        if 'CONFIG' in Environment.FASTAPI:
            if Environment.FASTAPI['CONFIG'] is not None:
                cls._app.extra.update(Environment.FASTAPI['CONFIG'])
            if 'OIDC' in Environment.Logins:
                from fastapi_oidc import FastAPIOIDC
                cls.openid = FastAPIOIDC()
                cls.openid.init_app(cls._app)
        return cls._app

    @classmethod
    def _load_statics(cls):
        """
        Load static files from static folder to /statics url
        """
        cls._app.mount(
            '/statics' if 'STATIC_URL' not in Environment.SERVER else Environment.SERVER['STATIC_URL'],
            StaticFiles(directory=Environment.SERVER['STATIC_PATH']),
            name="static"
        )

    @classmethod
    def _load_templates(cls):
        """
        Load templates from templates folder to be able to use them in fastapi.APIRouter.route decorator,
        server.add_route method or fastapi.APIRouter.route decorator
        """
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
        Start fastapi application using uvicorn. This method is blocking and is the main process.
        Can be stopped using keyboard signals
        :param args: needs arguments listening_address (nullable), listening_port (required) and pid (nullable)
        :type args: argparse.Namespace
        :return:
        """
        cls._args = args
        import uvicorn
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
        """
        Part that enable plugin to be loaded on working directory where the framework is called.
        Provides Process._app attribute to plugins as argument.
        """
        plugins.Load(
            server=cls._app,
        )

    @classmethod
    def load_routes(cls):
        """
        Part that loads all endpoints / routes in working directory where the framework is called.
        Provides Process._app attribute to plugins as argument.
        """
        ws.Route(cls._app)
        web.Route(cls._app)
        errors.Route(cls._app)

    @classmethod
    def load_middleware(cls):
        """
        Part that enable middlewares to be loaded on working directory where the framework is called.
        Provides Process._app attribute to plugins as argument.
        """
        middleware.Load(cls._app)

    @classmethod
    def load_socket_events(cls):
        """
        Part that loads all websocket events in working directory where the framework is called.
        Provides Process._app attribute to plugins as argument.
        """
        socket.Load(cls._app)

    @classmethod
    def pid(cls):
        """
        Creates a pid file for the current process.
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
        Removes the pid file.
        """
        import os
        os.unlink(cls._pidfile)

    @classmethod
    def get(cls):
        """
        Returns the current running fastapi instance
        :return:
        :rtype: fastapi.FastAPI
        """
        return cls._app

    @classmethod
    def stop(cls, code=0):
        """
        Shutdown the current process.
        :param code:
        :type: int
        :return:
        """
        if cls._args.pid:
            cls.shutdown()
        exit(code)

    @classmethod
    @outdated
    def login_manager(cls, login_manager=None):
        """
        outdated due to no fastapi support for a login manager.
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
