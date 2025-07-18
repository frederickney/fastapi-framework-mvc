class Route(object):
    """
    Class that will configure all web services based routes for the server
    """
    def __init__(self, server):
        """
        Constructor
        :param server: FastAPI server
        :type server: fastapi.FastAPI
        :return: Route object
        """
        import controllers
        server.add_route(path='/token', route=controllers.web.oauth.token, methods=["POST"], name='token')
        return
