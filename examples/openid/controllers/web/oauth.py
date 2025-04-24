# coding: utf-8
import json
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_framework_mvc.Server import Process
from pydantic import BaseModel
from starlette.datastructures import FormData

import fastapi_oidc

class Controller(object):

    @staticmethod
    async def token(request: Annotated[OAuth2PasswordRequestForm, Depends()]) -> JSONResponse:
        oidc_client: fastapi_oidc.FastAPIOIDC = Process.openid
        form_data: FormData = await request.form()
        user = oidc_client.token(form_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return JSONResponse(content=json.loads(user.get_id()), status_code=status.HTTP_200_OK)
