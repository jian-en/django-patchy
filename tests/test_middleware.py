from django.test import TestCase
from django.test import Client
from django.test import override_settings

from django.views.generic import View
from django.conf.urls import url
from django.http import HttpResponse

from patchy.utils import this_thread_is_sql_monitoring


class MockShortView(View):

    def get(self, request):
        return HttpResponse('hello world')


class MockLongView(View):

    """Mock a long consumed request
    """

    def get(self, request):
        import time
        time.sleep(1)
        return HttpResponse('hello')


class MockIgnoreView(View):

    """Mock a view that should be ignored
    """

    def get(self, request):
        import time
        time.sleep(2)
        return HttpResponse('hello')

urlpatterns = [
    url(r'^short/$', MockShortView.as_view()),
    url(r'^long/$', MockLongView.as_view()),
    url(r'^ignore/$', MockIgnoreView.as_view()),
]


@override_settings(ROOT_URLCONF='tests.test_middleware')
class TestRequestMiddleware(TestCase):

    def setUp(self):
        self.client = Client()

    def test_short_request(self):
        with self.settings(MIDDLEWARE_CLASSES=('patchy.middleware.LongRequestMiddleware',)):
            response = self.client.get('/short/')
            self.assertEqual(response.status_code, 200)
            elapsed = response.get('X-ELAPSED')
            self.assertTrue(float(elapsed) < 1)

    def test_long_request(self):
        with self.settings(MIDDLEWARE_CLASSES=('patchy.middleware.LongRequestMiddleware',)):
            response = self.client.get('/long/')
            self.assertEqual(response.status_code, 200)
            elapsed = response.get('X-ELAPSED')
            self.assertTrue(float(elapsed) > 1)

    def test_ignore_request(self):
        with self.settings(MIDDLEWARE_CLASSES=('patchy.middleware.LongRequestMiddleware',), PATCHY_LONG_REQUEST_IGNORE_URLS=[r'^/ignore']):
            self.client.get('/ignore/')
            self.assertFalse(this_thread_is_sql_monitoring())
