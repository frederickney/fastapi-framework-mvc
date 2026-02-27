# coding: utf-8


__author__ = 'Frederick NEY'


class Route(object):
    """
    Class that will configure all function used for handling requests error code
    """

    def __init__(self, srv):
        """
        Main entrypoint to load errors routes from working directory.
        Looks for server or Server module within working directory for any errorhandler or ErrorHandler file containing
        a Route class or method inside.
        :param srv: FastAPI instance
        :type srv: fastapi.FastAPI
        :return: Route object
        :rtype: Route
        """
        import logging
        import fastapi_framework_mvc.controllers as controllers
        srv.add_exception_handler(404, controllers.web.default.errors.http_404)
        srv.add_exception_handler(500, controllers.web.default.errors.http_500)
        try:
            import server
            server.errorhandler.Route(srv)
        except Exception as e:
            import os
            logging.warning("{}: {} in {}".format(__name__, e, os.getcwd()))
            try:
                import Server
                Server.ErrorHandler.Route(srv)
            except Exception as e:
                logging.warning("{}: Fallback to default error handler as : {} in {}".format(__name__, e, os.getcwd()))
        return
