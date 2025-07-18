# coding: utf-8


__author__ = 'Frederick NEY'

import logging

from fastapi_framework_mvc import Exceptions


def _load_yaml_file():
    return


def _load(file, loader):
    return loader.load(file)


def load_file(file):
    try:
        from . import json
        conf = _load(file, json)
    except Exceptions.ConfigExceptions.InvalidConfigurationFileError as e:
        logging.info(e.message)
        from . import yaml
        conf = _load(file, yaml)
    return conf


class Services(object):

    def __init__(self, name, registry):
        self.name = name,
        self.registry = registry


class Environment(object):
    Databases = {}
    SERVER = {}
    Logins = {}
    Services = {}
    FASTAPI = {}
    __default_runtime_change = False

    @staticmethod
    def _load(file, loader):
        return loader.load(file)

    @classmethod
    def reload(cls, file):
        try:
            from . import json
            conf = cls._load(file, json)
        except Exceptions.ConfigExceptions.InvalidConfigurationFileError as e:
            logging.info(e.message)
            from . import yaml
            conf = cls._load(file, yaml)
        cls.load_runtime(conf)
        cls.load_logins(conf)
        cls.load_services(conf)
        cls.FASTAPI = conf['FASTAPI'] if 'FASTAPI' in conf else cls.FASTAPI

    @classmethod
    def load(cls, file):
        try:
            from . import json
            conf = cls._load(file, json)
        except Exceptions.ConfigExceptions.InvalidConfigurationFileError as e:
            logging.info(e.message)
            from . import yaml
            conf = cls._load(file, yaml)
        cls.load_runtime(conf)
        cls.load_databases(conf)
        cls.load_logins(conf)
        cls.load_services(conf)
        cls.FASTAPI = conf['FASTAPI'] if 'FASTAPI' in conf else cls.FASTAPI
        cls.FASTAPI.setdefault('CONFIG', {})

    @classmethod
    def load_databases(cls, conf):
        try:
            for type in conf["DATABASES"]:
                if type != 'default':
                    cls.add_database(type, conf["DATABASES"][type])
                else:
                    cls.set_default_database(conf["DATABASES"][conf["DATABASES"][type]])
        except KeyError:
            cls.Databases = {}

    @classmethod
    def add_database(cls, db_type, db_conf):
        db = cls.Databases.get(db_type, None)
        if db is None:
            cls.Databases[db_type] = db_conf
        elif db is not None:
            logging.warning("Database '{}' already set".format(db_type))
            raise Exceptions.RuntimeExceptions.DatabaseChangeException(
                "Not permitted to change database '{}'  while app is running".format(db_type)
            )

    @classmethod
    def set_default_database(cls, db_conf):
        db = cls.Databases.get('default', None)
        if db is None and cls.__default_runtime_change is False:
            cls.Databases['default'] = db_conf
            cls.__default_runtime_change = True
        elif db is not None:
            logging.warning("Default database already set")
        else:
            raise Exceptions.RuntimeExceptions.DatabaseChangeException(
                "Not permitted to change default database while app is running"
            )

    @classmethod
    def load_logins(cls, conf):
        cls.Logins = conf['LOGINS'] if 'LOGINS' in conf else cls.Logins

    @classmethod
    def add_login(cls, login_name, login_conf):
        login = cls.Logins.get(login_name, None)
        if login is None:
            cls.Logins[login_name] = login_conf
        elif login is not None:
            logging.warning("Login service '{}' already set".format(login_name))
            raise Exceptions.RuntimeExceptions.LoginChangeException(
                "Not permitted to change login method '{}'  while app is running".format(login_name)
            )

    @classmethod
    def load_runtime(cls, conf):
        cls.SERVER = conf['SERVER']

    @classmethod
    def load_services(cls, conf):
        cls.Services.update(conf['SERVICES'] if 'SERVICES' in conf else cls.Services)

    @classmethod
    def add_service(cls, service_name, service_conf):
        service = cls.Services.get(service_name, None)
        if service is None:
            cls.Services[service_name] = service_conf
        elif service is not None:
            logging.warning("Service '{}' changed".format(service_name))
            cls.Services[service_name] = service_conf
