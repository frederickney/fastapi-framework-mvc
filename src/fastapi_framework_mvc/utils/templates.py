PYTHON_FILE_HEAD = '# coding: utf-8\n\n\n'

HTTP_ENTRY = """# coding: utf-8


class Route(object):
    \"\"\"
    Class that will configure all {} services based routes for the server
    \"\"\"
    def __init__(self, server):
        \"\"\"
        Constructor
        :param server: FastAPI instance
        :type server: fastapi.FastAPI
        :return: Route object
        \"\"\"
        import controllers
"""

HTTP_DEFAULT_ENTRY = """class Route(object):
    \"\"\"
    Class that will configure all {} services based routes for the server
    \"\"\"
    def __init__(self, server):
        \"\"\"
        Constructor
        :param server: FastAPI server
        :type server: fastapi.FastAPI
        :return: Route object
        \"\"\"
        import controllers
        server.add_route(path='/', route=controllers.web.home.index, methods=["GET"], name='home')
"""

HTTP_ERROR_HANDLER_ENTRY = """# coding: utf-8


class Route(object):
    \"\"\"
    Class that will configure all function used for handling requests error code
    \"\"\"

    def __init__(self, server):
        \"\"\"
        Constructor
        :param server: FastAPI server
        :type server: fastapi.FastAPI
        :return: Route object
        \"\"\"
        import controllers
{}
"""

WS_ENTRY = """# coding: utf-8


class Handler(object):

    def __init__(self, server):
        \"\"\"

        :param server:
        :type server: fastapi.FastAPI
        \"\"\"
        import controllers
"""

PLUGINS_ENTRY = """# coding: utf-8


class Load(object):

    def __init__(self, server):
        \"\"\"

        :param server:
        :type server: fastapi.FastAPI
        \"\"\"
        import controllers
"""

MIDDLEWARE_ENTRY = """# coding: utf-8


class Load(object):

    def __init__(self, server):
        \"\"\"

        :param server:
        :type server: fastapi.FastAPI
        \"\"\"
        import controllers
"""

ERROR_ENTRY = """        server.add_exception_handler({}, {})\n"""

BASE_ERROR = """
def http_{}(request, exc):
    return HTMLResponse(content="<h1>404</h1>", status_code=exc.status_code)
"""

BASE_ROUTER_CONTROLLER = """
# coding: utf-8

from fastapi import APIRouter
from fastapi import Request

router = APIRouter(prefix="/{PREFIX}")

class Controller(object):
    \"\"\"
    {PREFIX} Controller

    Class that handles all kind of allowed operation on {PREFIX}.

    Usualy get is for retrieving entries(y) with optional filter arguments, put is for creating new entry(ies),
    post is for updating entry(ies) and delete for deleting.
    \"\"\"
    
    #TODO add api route definition with api request model and return type
    @staticmethod
    @router.get("")
    def retrieve(fastapi_request: Request):
        #TODO implement your code here 
        pass
    
    #TODO add api route definition with api request model and return type
    @router.put("/create")
    def create(fastapi_request: Request):
        #TODO implement your code here 
        pass
        
    #TODO add api route definition with api request model and return type
    @router.post("/update")
    def create(fastapi_request: Request):
        #TODO implement your code here 
        pass
        
    #TODO add api route definition with api request model and return type
    @router.delete("/delete")
    def create(fastapi_request: Request):
        #TODO implement your code here 
        pass
"""

BASE_CONTROLLER = """# coding: utf-8


class Controller(object):

    @staticmethod
    def index():
        return
"""

BASE_HOME_CONTROLLER = """
class Controller(object):

    @staticmethod
    def index(request):
        return Process.templates.TemplateResponse(request=request, name="welcome.html")
"""

BASE_MIDDLEWARE = """
class {}(object):

    @classmethod
    def use(cls):
        \"\"\"
        :return: call to the decorated function
        \"\"\"

        def using(func):
            def decorator(*args, **kwargs):

                result = func(*args, **kwargs)
                return result

            return decorator

        return using

"""

IMPORTS = "from . import {}\n"

IMPORT_CONTROLLER = "from .{} import Controller as {}\n"

IMPORT_ROUTER_CONTROLLER = "from .{} import router as {}\n"

IMPORT_ERROR = "from .{} import http_{}\n"

HTTP_ERRORS = {
}

INSTALL_ROUTER = """        {}.include_router(router={})\n"""
INSTALL_PREFIXED_ROUTER = """        {}.include_router(prefix="{}", router={})\n"""
INSTALL_WEB_ROUTE = """        {}.add_route("/{}", {}, name="ui.{}")\n"""
INSTALL_API_ROUTE = """        {}.add_api_route("/api/{}", {}, name="api.{}")\n"""
INSTALL_WEBSOCKET_ROUTE = """        {}.add_websocket_route("/socket/{}", {}, name="socket.{}")\n"""
INSTALL_ERRORS_ROUTE= """        {}.add_exception_handler({}, {})\n"""

FASTAPI_RENDERING_IMPORT = "from fastapi_framework_mvc.core import Process\nfrom fastapi.responses import HTMLResponse\n\n"

FASTAPI_APP = "# coding: utf-8\n\nfrom fastapi_framework_mvc.app import app"

FASTAPI_FRAMEWORK_BASE_CONF = """SERVER:
    ENV: dev
    BIND:
        ADDRESS: localhost
        PORT: 4200
    WORKERS: uvicorn.workers.UvicornWorker
    CAPTURE: true
    THREADS_PER_CORE: 16
    LOG:
        DIR: log
        LEVEL: debug
"""
