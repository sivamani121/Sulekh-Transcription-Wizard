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
  words = models.CharField(max_length=999)
  tags = models.CharField(max_length=999)
  meaning = models.CharField(max_length=999,blank=True)
  status =models.IntegerField(default=0)
  lock= models.BooleanField(default=False)
  def __str__(self):
    return self.words
  def unlock(self):
    if self.lock:
      self.lock=False
      self.save()

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
class Annotated(models.Model):
  asent=models.ForeignKey(Sentence,on_delete=models.CASCADE)
  auser=models.ForeignKey(User,on_delete=models.CASCADE)
class Verified(models.Model):
  vsent=models.ForeignKey(Sentence,on_delete=models.CASCADE)
  vuser=models.ForeignKey(User,on_delete=models.CASCADE)
class DataSets(models.Model):
  datasetname = models.TextField(max_length=100)
  duser=models.ForeignKey(User,on_delete=models.CASCADE)
  lower= models.IntegerField(default=0)
  
  upper=models.IntegerField(default=0)
  def save(self, *args, **kwargs):
        if not self.id:
            t = DataSets.objects.values('upper').aggregate(Max('upper'))
            t = t['upper__max']
            if t is None:
                t = 0
            self.lower = t
            
            self.upper= Sentence.objects.aggregate(Max('id'))['id__max']
        super().save(*args, **kwargs)
