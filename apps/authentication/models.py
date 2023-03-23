# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=60,blank=True)
    username= models.CharField(max_length=60,blank=True,unique=True)
    score = models.BigIntegerField(default=0)
    password = models.TextField(max_length=200,default='password')
    email = models.CharField(max_length=70,blank=True)
    tag = models.IntegerField(default=0)
    def _str_(self) -> str:
        t= str(self.id)+"  "+self.name
        return t


class Users(models.Model):
    name = models.CharField(max_length=60,blank=True)
    username= models.CharField(max_length=60,blank=True)
    score = models.BigIntegerField(default=0)
    password = models.TextField(max_length=200,default='password')
    email = models.CharField(max_length=70,blank=True)
    tag = models.IntegerField(default=0)
    def _str_(self) -> str:
        t= str(self.id)+"  "+self.name
        return t