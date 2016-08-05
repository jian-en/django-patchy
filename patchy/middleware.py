"""
Custom middleware
"""
import time
import logging
import re

from django.conf import settings

from .utils import sql_unmonitoring_this_thread


logger = logging.getLogger(__name__)


class LongRequestMiddleware(object):

    """Long request middleware, remember to put it first
    """

    def __init__(self):
        """Initialize timeout with PATCHY_LONG_REQUEST_TIMEOUT with default to one second
        """
        self.ignore_url_patterns = getattr(settings, 'PATCHY_LONG_REQUEST_IGNORE_URLS', list())
        # skip any sql timeout mornitoring if lr is ignored
        self.stick_to_lr = getattr(settings, 'PATCHY_STICK_TO_LR', True)
        self.timeout = getattr(settings, 'PATCHY_LONG_REQUEST_TIMEOUT', 1)

    def process_request(self, request):
        """record the time in
        """
        self._start = time.time()

        self.url_matched = False
        for url_pattern in self.ignore_url_patterns:
            # if the current path in ignored url list, just ignore it
            if re.match(url_pattern, request.path):
                self.url_matched = True
                if self.stick_to_lr:
                    sql_unmonitoring_this_thread()
                break

    def process_response(self, request, response):
        """record the time out
        """
        self._end = time.time()
        elapsed = self._end - self._start
        if elapsed > self.timeout and not self.url_matched:
            # too long and log to target
            logger.error('[Long Request]Path: %s, Time: %s s' % (request.path, elapsed))

        response['X-ELAPSED'] = elapsed
        return response
