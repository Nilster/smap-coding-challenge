# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.IntegerField(unique=True)
    area = models.CharField(max_length=5)
    tariff =  models.CharField(max_length=5)

    def __str__(self):
        return str(self.user_id)

class Usage(models.Model):
    user_id = models.ForeignKey(User,to_field='user_id',on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    consumption = models.DecimalField(max_digits=10, decimal_places=1)
    filename = models.FilePathField()

    def __str__(self):
        return str(self.consumption)