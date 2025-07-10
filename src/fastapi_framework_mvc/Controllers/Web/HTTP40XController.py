# coding: utf-8


__author__ = 'Frederick NEY'


from fastapi.responses import HTMLResponse
from fastapi_framework_mvc.Server import Process


async def page_or_error404(request, exc):
    if request.url.path == '/':
        return Process.templates.TemplateResponse(request=request, name="welcome.html")
    return Process.templates.TemplateResponse(request=request, name="404.html" , status_code=exc.status_code, context={'error': exc})
