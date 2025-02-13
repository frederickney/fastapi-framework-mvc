# coding: utf-8


__author__ = 'Frederick NEY'


from fastapi.responses import HTMLResponse


async def page_or_error404(request, exc):
    return HTMLResponse(content="<h1>404</h1>", status_code=exc.status_code)
