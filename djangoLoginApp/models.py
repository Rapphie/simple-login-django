from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    username = models.CharField(max_length=255, blank=False, null=False, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=20)
