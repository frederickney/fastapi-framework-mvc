# coding: utf-8

from pydantic import BaseModel
from typing import Optional, Any
from logging import WARNING

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