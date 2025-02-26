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
        return
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
        return
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
        return
"""

WS_ENTRY = """# coding: utf-8


class Handler(object):

    def __init__(self, app):
        \"\"\"

        :param app:
        :type app: fastapi.FastAPI
        \"\"\"
        import controllers
        return
"""

ERROR_ENTRY = """        server.add_exception_handler({}, {})\n"""

BASE_ERROR = """
def http_{}(request, exc):
    return HTMLResponse(content="<h1>404</h1>", status_code=exc.status_code)
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

IMPORT_ERROR = "from .{} import http_{}\n"

HTTP_ERRORS = {
    404: 'controllers.web.errors.http_404',
    500: 'controllers.web.errors.http_500'
}

FLASK_RENDERING_IMPORT = "from fastapi_framework_mvc.Server import Process\nfrom fastapi.responses import HTMLResponse\n\n"

FLASK_FRAMEWORK_BASE_CONF = """SERVER:
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

DATABASES: {{}}

FASTAPI:
  CONFIG: {{}}
"""
