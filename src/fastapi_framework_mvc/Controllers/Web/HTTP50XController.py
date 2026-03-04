# coding: utf-8


__author__ = 'Frederick NEY'


import logging
from fastapi.responses import HTMLResponse
from fastapi_framework_mvc.Server import Process
from fastapi_framework_mvc.Deprecation import module_deprecation
module_deprecation(__name__, 'fastapi_framework_mvc.controllers.web.default.errors.http_50x', '1.3.0')

async def error500(request, exc):
    return Process.templates.TemplateResponse(request=request, context={'message': exc},  name="500.html", status_code=500)
    
