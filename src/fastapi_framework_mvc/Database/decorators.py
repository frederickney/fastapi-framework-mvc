# coding: utf-8


__author__ = 'Frederick NEY'

import os
import logging
import sqlalchemy

from .driver import Driver


def _rollback():
    for session in Driver.sessions:
        try:
            session.rollback()
        except Exception as e:
            logging.error(e)
    try:
        Driver.session.rollback()
    except Exception as e:
        logging.error(e)


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