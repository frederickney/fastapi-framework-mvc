# coding: utf-8


__author__ = 'Frederick NEY'


import logging
from fastapi.responses import HTMLResponse
from fastapi_framework_mvc.server import Process


async def http_500(request, exc):
    return Process.templates.TemplateResponse(request=request, context={'message': exc},  name="500.html", status_code=500)
    
