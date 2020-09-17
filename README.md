# Django Patchy

[![PyPI version](https://badge.fury.io/py/djangopatchy.svg)](https://badge.fury.io/py/djangopatchy)

**Useful django app and utils to develop large-scale web app**

# Requirements

* Python (2.7)
* Django (1.8, 1.9)

# Installation

Install using `pip`...

    pip install djangopatchy

# Middlewares

## LongRequestMiddleware

Let's add a middleware to calculate the time elapse for each request

1. Add a middleware at the top:

```python
MIDDLEWARE_CLASSES = (
    'patchy.middleware.LongRequestMiddleware',
    ...
)
```

2. Add logger handler with `patchy.middleware`:

Example:

```python
'patchy.middleware': {
    'handlers': ['sentry'],
    'level': 'ERROR',
    'propagate': True
}
```

3. Set the timeout threshold in settings(default to 1 second):

```python
PATCHY_LONG_REQUEST_TIMEOUT = 2  # set the timeout to 2 seconds
```

Results:

* For each web request, it has a header variable `X-ELAPSED` in seconds to indicate the time elapse. 

```bash
X-ELAPSED: 0.005 # it means the request costs 5 ms
```

* If it exceeds the `PATCHY_LONG_REQUEST_TIMEOUT` a error log message will be sent.

4. Add some urls to ignore list(optional), regular expression is supported.

```python
PATCHY_LONG_REQUEST_IGNORE_URLS = [
    r'^/_admin/.*$',
]
```

# Utilities

## long_sql_execute_wrapper

Let us rewrite the CursorWrapper.execute to calculate the sql process time

1. Add the python snippets in the `djangoproject/__init__.py`
```python
# rewrite the sql operation method
from django.db.backends import utils
from patchy.utils import long_sql_execute_wrapper
utils.CursorWrapper.execute = long_sql_execute_wrapper
```

2. Add logger handler with `patchy.utils`:

Example:

```python
'patchy.utils': {
    'handlers': ['sentry'],
    'level': 'ERROR',
    'propagate': True
}
```

3. Set the timeout threshold in settings(default to 0.05 seond, which is 50 miliseconds):

```python
PATCHY_LONG_SQL_TIMEOUT = 0.01  # set the timeout to 10 miliseconds
```

Result:

* If the sql operation exceeds the `PATCHY_LONG_SQL_TIMEOUT` a error log message will be sent.

4. no\_sql\_monitoring

`no_sql_monitoring` is a decorator for wrapping code to skip sql monitoring.

```python
from patchy.utils import no_sql_monitoring

@no_sql_monitoring
def transaction_status(request, transaction_no):
    transaction = Transaction.objects.get(transaction_no=transaction_no)

    return ResponseBuilder.build_success_json_response(
        msg='查询订单成功',
        data={
            'transaction_no': transaction_no,
            'transaction_status': transaction.transaction_status
    })
```
