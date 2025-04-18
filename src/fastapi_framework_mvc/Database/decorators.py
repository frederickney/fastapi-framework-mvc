# coding: utf-8


__author__ = 'Frederick NEY'

import logging
import sqlalchemy

from .driver import Driver


def secured(prop):
    def load(obj):
        def decorator(*args, **kwargs):
            object = obj(*args, **kwargs)
            logging.warning('Loading secure function')

            def set_id(object, value):
                property()
                from fastapi_framework_mvc.Exceptions.QueryExceptions import PrimaryKeyChangeException
                raise PrimaryKeyChangeException(
                    "Trying to change read only primary key id of {}[{}] by {}".format(
                        object.__class__.__name__,
                        object.get_id, value)
                )

            logging.warning('Defining secured property')
            # = object.__getattribute__(property)
            object.__setattr__(object, property(prop.get_id, set_id))
            return object

        return decorator

    return load


def _rollback():
    for session in Driver.sessions:
        try:
            session.rollback()
        except Exception as e:
            logging.error(e)
    try:
        Driver.session.rollback()
        return func(*args, **kwargs)
    except Exception as e:
        logging.error(e)
        raise e


def safe(func):

    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlalchemy.exc.PendingRollbackError as e:
            logging.warning(e)
            _rollback() 
            return func(*args, **kwargs)
        except sqlalchemy.exc.OperationalError as e:
            logging.warning(e)
            Driver.reconnect_all()
            return func(*args, **kwargs)

    return decorated


class Database(object):
    cls: object = None

    def load(self, cls):

        def decorator(*args, **kwargs):
            instance = cls(*args, **kwargs)
            self.cls = instance
            return instance

        return decorator

    def use(self, databases=['default']):

        def using(func):
            def decorator(*args, **kwargs):
                logging.info('connecting')
                sessions = dict()
                for db_name in databases:
                    sessions[db_name] = Driver.start_session_by_name(db_name)
                setattr(self.cls, 'sessions', sessions)
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    logging.error(e)
                    result = None
                logging.info(self.cls)
                for name, session in sessions.items():
                    session.close()

                logging.info('disconnecting')
                return result

            return decorator

        return using

    @staticmethod
    def use_db(databases=['default']):
        def using(func):
            def decorator(*args, **kwargs):
                sessions = dict()
                for db_name in databases:
                    sessions[db_name] = Driver.get_session_by_name(db_name)
                    kwargs.setdefault('sessions', sessions)
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    logging.error("{}: {}".format(__name__, e))
                    result = None
                return result

            return decorator

        return using

    @staticmethod
    def safe_use_db(databases=['default']):
        def using(func):
            def decorator(*args, **kwargs):
                logging.info('connecting')
                sessions = dict()
                for db_name in databases:
                    sessions[db_name] = Driver.start_session_by_name(db_name)
                    kwargs.setdefault('sessions', sessions)
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    logging.error("{}: {}".format(__name__, e))
                    result = None
                for name, session in sessions.items():
                    session.close()
                logging.info('disconnecting')
                return result

            return decorator

        return using
