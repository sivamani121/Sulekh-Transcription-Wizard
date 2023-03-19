# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models

# Create your models here.
class Annotator(models.Model):
    aid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    username= models.CharField(max_length=60)
    score = models.BigIntegerField()
    logged_in =models.BooleanField(default=False)
    password = models.TextField(max_length=200)
    mobileno = models.CharField(max_length=20)
    email = models.CharField(max_length=70)
    def __str__(self) -> str:
        t= str(self.id)+"  "+self.name
        return t


class Verifier(models.Model):
    vid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    score = models.BigIntegerField()
    username= models.CharField(max_length=60)
    logged_in =models.BooleanField(default=False)
    password = models.TextField(max_length=200)
    mobileno = models.CharField(max_length=20)
    email = models.CharField(max_length=70)
    def __str__(self) -> str:
        t= str(self.id)+"  "+self.name
        return t


class Confirmer(models.Model):
    vid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    username= models.CharField(max_length=60)
    logged_in =models.BooleanField(default=False)
    password = models.TextField(max_length=200)
    mobileno = models.CharField(max_length=20)
    email = models.CharField(max_length=70)
    def __str__(self) -> str:
        t= str(self.id)+"  "+self.name
        return t