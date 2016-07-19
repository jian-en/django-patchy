from django.test import TestCase
from django.test import Client
from django.test import override_settings

from django.views.generic import View
from django.conf.urls import url
from django.http import HttpResponse


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

urlpatterns = [
    url(r'^short/$', MockShortView.as_view()),
    url(r'^long/$', MockLongView.as_view()),
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
