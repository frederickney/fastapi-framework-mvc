# coding: utf-8


__author__ = 'Frederick NEY'


class Load(object):
    """
    Class that will load plugins from working directory from where
    the fastapi_framework_mvc package is called.
    """

    def __init__(cls, **kwargs):
        """
        Main entrypoint to load plugins from working directory.
        Looks for server or Server module within working directory for any plugins or Plugins file containing
        a Load class.
        :param srv: FastAPI instance
        :type server: fastapi.FastAPI
        :return: Load object
        :rtype: Load
        """
        import logging
        try:
            import server
            server.plugins.Load(**kwargs)
        except Exception as e:
            import os
            logging.debug("{}: {} in {}".format(__name__, e, os.getcwd()))
            try:
                import Server
                Server.Plugins.Load(**kwargs)
            except Exception as e:
                import os
                logging.debug("{}: {} in {}".format(__name__, e, os.getcwd()))
        return
