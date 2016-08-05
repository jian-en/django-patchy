from django.test import TestCase
from django.test import Client
from django.test import override_settings

from django.views.generic import View
from django.http import HttpResponse
from django.conf.urls import url

from .models import OneFieldModel
from patchy.utils import sql_monitoring_this_thread


class MockView(View):

    def get(self, request):
        num = OneFieldModel.objects.count()
        return HttpResponse('The total num of records is %d.' % num)


class NoSqlMockView(View):
    from patchy.utils import no_sql_monitoring

    @no_sql_monitoring
    def get(self, request):

        return HttpResponse('hello')


urlpatterns = [
    url(r'^$', MockView.as_view()),
    url(r'^nosql/$', NoSqlMockView.as_view()),
]


@override_settings(ROOT_URLCONF='tests.test_utils')
@override_settings(PATCHY_LONG_SQL_TIMEOUT=0.000000001)
class TestLongSQL(TestCase):

    def setUp(self):
        sql_monitoring_this_thread()
        self.client = Client()

    def test_sql_request(self):
        # replace the orig wrapper
        from django.db.backends import utils
        from patchy.utils import long_sql_execute_wrapper
        utils.CursorWrapper.execute = long_sql_execute_wrapper

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


@override_settings(ROOT_URLCONF='tests.test_utils')
@override_settings(PATCHY_LONG_SQL_TIMEOUT=0.0000000001)
class TestIgnoreSQL(TestCase):

    def setUp(self):
        sql_monitoring_this_thread()
        self.client = Client()

    def test_no_sql_view(self):
        # replace the orig wrapper
        from django.db.backends import utils
        from patchy.utils import long_sql_execute_wrapper
        utils.CursorWrapper.execute = long_sql_execute_wrapper

        response = self.client.get('/nosql/')
        self.assertEqual(response.status_code, 200)
