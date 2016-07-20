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

2. Add logger handler with `pathcy.middleware`:

Example:

```python
'patchy.middleware': {
    'handlers': ['sentry'],
    'level': 'ERROR',
    'propagate': True
}
```

3. Set the timeout threshold in settings:

```python
PATCHY_LONG_REQUEST_TIMEOUT = 2  # set the timeout to 2 seconds
```

Results:

* For each web request, it has a header variable `X-ELAPSED` in seconds to indicate the time elapse. 

```bash
X-ELAPSED: 0.005 # it means the request costs 5 ms
```

* If it exceeds the `PATCHY_LONG_REQUEST_TIMEOUT` a error log message will be sent.
