# Django Patchy

[![pypi-version][pypi]]

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

Add a middleware at the top:

```python
MIDDLEWARE_CLASSES = (
    'patchy.middleware.LongRequestMiddleware',
    ...
)
```

* Then for each web request, it has a header `X-ELAPSED` in seconds to indicate the time elapse. 

* And a setting variable called `PATCHY_LONG_REQUEST_TIMEOUT` is provided. It can be set in the settings.py file. It defaults to 1 second. 

* If it exceeds the `PATCHY_LONG_REQUEST_TIMEOUT` a error log message will be sent.
