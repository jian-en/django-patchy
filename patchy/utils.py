import time
import logging

from django.conf import settings
from django.db.backends.utils import CursorWrapper

logger = logging.getLogger(__name__)

try:
    TIMEOUT = settings.PATCHY_LONG_SQL_TIMEOUT
except AttributeError:
    TIMEOUT = 0.05  # 50 ms


original = CursorWrapper.execute


def long_sql_execute_wrapper(*args, **kwargs):
    try:
        start = time.time()
        result = original(*args, **kwargs)
        end = time.time()
        return result
    finally:
        duration = end - start
        if duration > TIMEOUT:
            try:
                message = 'SQL: (%s), Args: (%s), Execution time: %.6fs' % (args[1], args[2], duration)
            except IndexError:
                message = 'SQL: (%s), Args: (), Execution time: %.6fs' % (args[1], duration)
            logger.error(message)
