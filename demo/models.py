from django.contrib.auth.models import User
from django.db import models
from demo.test_interface import TestProjectInterface


class ProjectTest(models.Model, TestProjectInterface):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=150)


class City(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.name


class Country(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=255)
    capital = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.name
