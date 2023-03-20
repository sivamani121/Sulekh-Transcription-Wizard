# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models

# Create your models here.
class Users(models.Model):
    aid = models.BigIntegerField(primary_key=True,blank=True)
    name = models.CharField(max_length=60)
    username= models.CharField(max_length=60,blank=True)
    score = models.BigIntegerField(default=0)
    password = models.TextField(max_length=200)
    mobileno = models.CharField(max_length=20,blank=True)
    email = models.CharField(max_length=70,blank=True)
    tag = models.IntegerField(default=0)
    def _str_(self) -> str:
        t= str(self.id)+"  "+self.name
        return t