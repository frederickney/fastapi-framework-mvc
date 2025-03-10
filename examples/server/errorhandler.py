# coding: utf-8


class Route(object):
    """
    Class that will configure all function used for handling requests error code
    """

    def __init__(self, server):
        """
        Constructor
        :param server: FastAPI server
        :type server: fastapi.FastAPI
        :return: Route object
        """
        import controllers
        server.add_exception_handler(404, controllers.web.errors.http_404)
        server.add_exception_handler(500, controllers.web.errors.http_500)

        return
