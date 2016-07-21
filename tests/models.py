from django.db import models


class OneFieldModel(models.Model):
    char_field = models.CharField(max_length=100)
