# coding: utf-8


__author__ = 'Frederick NEY'


from fastapi.responses import HTMLResponse


async def error500(request, exc):
    return HTMLResponse(content="<h1>500</h1>", status_code=exc.status_code)
