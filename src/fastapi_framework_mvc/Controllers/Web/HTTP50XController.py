# coding: utf-8


__author__ = 'Frederick NEY'


import logging
from fastapi.responses import HTMLResponse
from fastapi_framework_mvc.Server import Process


async def error500(request, exc):
    return Process.templates.TemplateResponse(request=request, context={'message': exc},  name="500.html", status_code=500)
    
