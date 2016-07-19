"""
Custom middleware
"""
import time
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class LongRequestMiddleware(object):

    """Long request middleware, remember to put it first
    """

    def __init__(self):
        """Initialize timeout with PATCHY_LONG_REQUEST_TIMEOUT with default to one second
        """
        try:
            self.timeout = settings.PATCHY_LONG_REQUEST_TIMEOUT
        except AttributeError:
            self.timeout = 1

    def process_request(self, request):
        """record the time in
        """
        self._start = time.time()

    def process_response(self, request, response):
        """record the time out
        """
        self._end = time.time()
        elapsed = self._end - self._start
        if elapsed > self.timeout:
            # too long and log to target
            logger.error('[Long Request]Path: %s, Time: %s s' % (request.path, elapsed))
        response['X-ELAPSED'] = elapsed
        return response
