# coding: utf-8

from logging import WARNING
from typing import Optional, Any, Union

from pydantic import BaseModel


class _Bind(BaseModel):
    ADDRESS: str = '0.0.0.0'
    PORT: int = 8080


class _Log(BaseModel):
    DIR: str
    LEVEL: str = WARNING


class Server(BaseModel):
    ENV: str
    BIND: _Bind
    WORKERS: str = "uvicorn.workers.UvicornWorker"
    CAPTURE: bool
    THREADS_PER_CORE: int
    LOG: _Log


class Database(BaseModel):
    driver: str
    user: Optional[str] = None
    password: Optional[str] = None
    database: str
    address: str
    models: str
    params: dict[str, Any]
    dialects: dict[str, Any]
    readonly: bool


class FastApiConf:
    CONF: dict[str, Any]


class Conf:
    SERVER: Server
    FASTAPI: FastApiConf
    DATABASES: dict[str, Union[Database, str]]
    SERVICES: dict[str, Any]