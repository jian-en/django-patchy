import time
import logging
import threading
from functools import wraps

from django.conf import settings
from django.db.backends.utils import CursorWrapper

logger = logging.getLogger(__name__)

_locals = threading.local()


def this_thread_is_sql_monitoring():
    return getattr(_locals, 'sql_monitoring', True)


def sql_monitoring_this_thread():
    _locals.sql_monitoring = True


def sql_unmonitoring_this_thread():
    _locals.sql_monitoring = False


class NoSQLMonitoring(object):

    def __call__(self, func):
        @wraps(func)
        def decorator(*args, **kw):
            with self:
                return func(*args, **kw)
        return decorator

    def __enter__(self):
        _locals.patchy_outer_scope = this_thread_is_sql_monitoring()
        sql_unmonitoring_this_thread()

    def __exit__(self, type, value, tb):
        if _locals.patchy_outer_scope:
            sql_monitoring_this_thread()

no_sql_monitoring = NoSQLMonitoring()


original = CursorWrapper.execute


def long_sql_execute_wrapper(*args, **kwargs):
    TIMEOUT = getattr(settings, 'PATCHY_LONG_SQL_TIMEOUT', 0.05)
    try:
        start = time.time()
        result = original(*args, **kwargs)
        return result
    finally:
        end = time.time()
        duration = end - start
        if duration > TIMEOUT and this_thread_is_sql_monitoring():
            try:
                message = 'SQL: (%s), Args: (%s), Execution time: %.6fs' % (args[1], args[2], duration)
            except IndexError:
                message = 'SQL: (%s), Args: (), Execution time: %.6fs' % (args[1], duration)
            logger.error(message)
