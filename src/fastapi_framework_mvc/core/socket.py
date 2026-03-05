# coding: utf-8


__author__ = 'Frederick NEY'


class Load(object):
    """
    Class that will load websocket events from working directory from where
    the fastapi_framework_mvc package is called.
    """

    def __init__(self, socketio):
        """
        Main entrypoint to load plugins from working directory.
        Looks for server or Server module within working directory for any socket or Socket file containing
        a Handle class or method inside.
        :param socketio: FastAPI instance
        :type socketio: fastapi.FastAPI
        :return: Handler object
        :rtype: Load
        """
        import logging
        try:
            import server
            server.socket.Handler(socketio)
        except Exception as e:
            import os
            logging.warning("{}: {} in {}".format(__name__, e, os.getcwd()))
            try:
                import Server
                Server.Socket.Handler(socketio)
            except Exception as ie:
                import traceback
                logging.warning("{}: {} in {}".format(__name__, ie, os.getcwd()))
        return
