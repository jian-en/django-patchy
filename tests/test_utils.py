from django.test import TestCase
from django.test import Client
from django.test import override_settings

from django.views.generic import View
from django.http import HttpResponse
from .models import OneFieldModel
from django.conf.urls import url


class MockView(View):

    def get(self, request):
        num = OneFieldModel.objects.count()
        return HttpResponse('The total num of records is %d.' % num)


urlpatterns = [
    url(r'^$', MockView.as_view()),
]


@override_settings(ROOT_URLCONF='tests.test_utils')
@override_settings(PATCHY_LONG_SQL_TIMEOUT=0.000000001)
class TestLongSQL(TestCase):

    def setUp(self):
        self.client = Client()

    def test_sql_request(self):
        # replace the orig wrapper
        from django.db.backends import utils
        from patchy.utils import long_sql_execute_wrapper
        utils.CursorWrapper.execute = long_sql_execute_wrapper

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
