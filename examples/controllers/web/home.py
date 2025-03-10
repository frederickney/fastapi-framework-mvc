# coding: utf-8


from fastapi_framework_mvc.Server import Process
from fastapi.responses import HTMLResponse


class Controller(object):

    @staticmethod
    def index(request):
        return Process.templates.TemplateResponse(request=request, name="welcome.html")
