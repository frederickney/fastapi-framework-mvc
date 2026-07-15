# coding: utf-8


__author__ = 'Frederick NEY'


class Route(object):
    """
    Class that will configure all web services based routes for the server
    """

    def __init__(self, srv):
        """
        Main entrypoint to load http rest api routes from working directory.
        Looks for server or Server module within working directory for any ws or WS file containing
        a Route class.
        :param srv: FastAPI instance
        :type srv: fastapi.FastAPI
        :return: Route object
        :rtype: Route
        """
        import logging
        try:
            import server
            server.ws.Route(srv)
        except Exception as e:
            import os
            logging.warning("{}: {} in {}".format(__name__, e, os.getcwd()))
            try:
                import Server
                Server.WS.Route(srv)
            except Exception as ie:
                import traceback
                logging.warning("{}: {} in {}".format(__name__, ie, os.getcwd()))
        return
