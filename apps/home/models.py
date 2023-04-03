# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
# from authentication.models import Users
from datetime import datetime
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.
class Sentence(models.Model):
  words = models.CharField(max_length=999999)
  tags = models.CharField(max_length=999999)
  meaning = models.CharField(max_length=99999,blank=True)
  status =models.IntegerField(default=0)
  def __str__(self):
    return self.words
    

class Answered(models.Model):
  sentno = models.ForeignKey(Sentence,on_delete=models.CASCADE)
  userid = models.ForeignKey(User,on_delete=models.DO_NOTHING)
  updatedate = models.DateTimeField(default=datetime.now,blank=True)
class sent_req(models.Model):
  sentence = models.ForeignKey(Sentence,on_delete=models.CASCADE)
  user = models.ForeignKey(User,on_delete=models.CASCADE)
 
  
