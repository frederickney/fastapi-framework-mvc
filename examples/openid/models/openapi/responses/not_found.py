# coding: utf-8

__AUTHOR__ = "Frédérick NEY"

from pydantic import BaseModel


class NotFound(BaseModel):
    details: str

