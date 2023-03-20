# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Data(models.Model):
  words = models.CharField(max_length=999999)
  tags = models.CharField(max_length=999999)
  meaning = models.CharField(max_length=99999)
