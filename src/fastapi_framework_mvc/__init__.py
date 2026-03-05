# coding: utf-8


__author__ = "Frederick NEY"

import sys
from . import Database as database
from .Database import decorators
from . import Config as config
from . import Deprecation as deprecation
from . import Exceptions as exceptions
from . import Libs as libs
from . import Utils as utils
from . import Server as core


def set_upper_version_module():
    sys.modules["fastapi_framework_mvc.utils"] = utils
    sys.modules["fastapi_framework_mvc.database"] = database
    sys.modules["fastapi_framework_mvc.database.decorators"] = decorators
    sys.modules["fastapi_framework_mvc.deprecation"] = deprecation
    sys.modules["fastapi_framework_mvc.exceptions"] = exceptions
    sys.modules["fastapi_framework_mvc.libs"] = libs
    sys.modules["fastapi_framework_mvc.utils"] = utils
    sys.modules["fastapi_framework_mvc.core"] = core
    sys.modules["fastapi_framework_mvc.config"] = config