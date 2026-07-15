# coding: utf-8


__author__ = 'Frederick NEY'

from fastapi_framework_mvc.core import Process


async def http_404(request, exc):
    if request.url.path == '/':
        return Process.templates.TemplateResponse(request=request, name="welcome.html")
    return Process.templates.TemplateResponse(
        request=request,
        name="404.html",
        status_code=exc.status_code,
        context={'error': exc}
    )
