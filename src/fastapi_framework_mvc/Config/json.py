# coding: utf-8


__author__ = 'Frederick NEY'

import logging
import fastapi_framework_mvc.Exceptions as Exceptions
from fastapi_framework_mvc.Deprecation import Future

def _load(file):
    """
    :deprecated : will be removed on version 1.2.0
    """
    import os.path, json
    from json import JSONDecodeError
    if isinstance(file, str):
        if os.path.exists(file):
            if os.path.isfile(file):
                fd = open(file)
                try:
                    content = json.load(fd)
                    fd.close()
                    logging.warning(
                        "If you see this, that means you are using a soon to be removed file format.\n"
                        "And the above warning is related to your configuration.\n"
                        "Consider using the yaml file format for better environ and secrets variable load"
                    )
                    return content
                except JSONDecodeError as e:
                    raise Exceptions.ConfigExceptions.InvalidConfigurationFileError(
                        file + ": Expected json file format."
                    )
                    fd.close()
            else:
                raise Exceptions.ConfigExceptions.NotAConfigurationFileError(file + ": Not a valid file.")
        else:
            raise Exceptions.ConfigExceptions.NotAConfigurationFileError(file + ": File did not exist.")
    else:
        raise Exceptions.ConfigExceptions.NotAConfigurationFileError(
            "Expected " + type(str) + ", got " + type(file) + "."
        )

@Future.remove("1.2.0")
def load(file):
    return _load(file)
