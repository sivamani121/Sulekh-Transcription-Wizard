# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
# from authentication.models import Users
from datetime import datetime
from django.conf import settings
from django.db.models import Max
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
class Confirmed(models.Model):
  csent=models.ForeignKey(Sentence,on_delete=models.CASCADE)
  cuser = models.ForeignKey(User,on_delete=models.CASCADE)
  
class DataSets(models.Model):
  datasetname = models.TextField(max_length=100)
  lower= models.IntegerField(default=0)
  upper=models.IntegerField(default=0)
  def save(self, *args, **kwargs):
        if not self.id:
            self.lower = DataSets.objects.aggregate(Max('upper'))['upper__max']
            self.upper= min(Sentence.objects.aggregate(Max('id'))['id__max'])
        super().save(*args, **kwargs)
class Assigned(models.Model):
  user_anno = models.ForeignKey(User,on_delete=models.DO_NOTHING)
  lower= models.IntegerField(default=0)
  upper=models.IntegerField(default=0)
  def save(self, *args, **kwargs):
        if not self.id:
            self.lower = Assigned.objects.aggregate(Max('upper'))['upper__max']
            self.upper= min(self.lower+50,Sentence.objects.aggregate(Max('id'))['id__max'])

        super().save(*args, **kwargs)