# coding: utf-8

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi_oidc.client import FastAPIOIDC
from fastapi_framework_mvc.Database.decorators import safe
from fastapi_framework_mvc.Server import Process

from models.openapi.responses import NotFound


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

class Openid(object):

    @safe           # for datatabase access
    @staticmethod
    def index(token: Annotated[str, Depends(oauth2_scheme)]):
        openid: FastAPIOIDC = Process.openid
        user = openid.user(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalid or expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return NotFound(details='empty')


class Controller(Openid):

    @classmethod
    async def index(cls, token: Annotated[str, Depends(oauth2_scheme)]):
        return super(cls, Controller).index(token)
