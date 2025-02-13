# coding: utf-8


__author__ = 'Frederick NEY'


class Load(object):

    def __init__(self, socketio):
        """

        :param socketio:
        :type socketio: fastapi.FastAPI
        :return: Handler object
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
                logging.warning("{}: Fallback to default controller as: {} in {}".format(__name__, ie, os.getcwd()))
                import fastapi_framework_mvc.Controllers as Controller
        return
