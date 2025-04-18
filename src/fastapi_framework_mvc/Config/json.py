# coding: utf-8


__author__ = 'Frederick NEY'

import fastapi_framework_mvc.Exceptions as Exceptions


def _load(file):
    import os.path, json
    from json import JSONDecodeError
    if isinstance(file, str):
        if os.path.exists(file):
            if os.path.isfile(file):
                fd = open(file)
                try:
                    content = json.load(fd)
                    fd.close()
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


def load(file):
    return _load(file)
