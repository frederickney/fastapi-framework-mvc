# coding: utf-8


class Route(object):
    """
    Class that will configure all ws services based routes for the server
    """
    def __init__(self, server):
        """
        Constructor
        :param server: FastAPI instance
        :type server: fastapi.FastAPI
        :return: Route object
        """
        import controllers
        from models.openapi.responses import NotFound, Unauthorized
        server.add_api_route(
            path='/api/openid/',
            endpoint=controllers.ws.openid.index,
            methods=['GET'],
            name='api.content',
            response_model=NotFound,
            responses={401: {"model": Unauthorized}}
        )
        return
