# coding: utf-8


from fastapi_framework_mvc.Server import Process
from fastapi.responses import HTMLResponse


def http_404(request, exc):
    return HTMLResponse(content="<h1>404</h1>", status_code=exc.status_code)
