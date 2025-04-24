import logging
import fastapi_oidc.client 
from fastapi_framework_mvc.Server import Process

class Load(object):
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
        Process.openid = fastapi_oidc.client.FastAPIOIDC(server)
        return

