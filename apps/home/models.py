# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from apps.authentication.models import Annotator,Verifier,Confirmer 



class Sentence(models.Model):
    sno = models.BigIntegerField(primary_key=True)
    noofwords= models.IntegerField()
    status = models.IntegerField(models.constraints(MaxValueValidator=3,MinValueValidator=0))
    def __str__(self) -> str:
        return str(self.sno)

class Words(models.Model):
    wdno = models.IntegerField()
    sno = models.ForeignKey(Sentence,on_delete=models.CASCADE)
    tag = models.CharField(max_length=1)
    word = models.CharField(max_length=60)
    ans = models.CharField()
    def __str__(self) -> str:
        return str(self.word)


class Answered(models.Model):
    aid = models.ForeignKey(Annotator,on_delete=models.DO_NOTHING)
    sno = models.ForeignKey(Sentence,on_delete=models.CASCADE)
class Verified(models.Model):
    vid = models.ForeignKey(Verifier,on_delete=models.DO_NOTHING)
    sno = models.ForeignKey(Sentence,on_delete=models.CASCADE)
class Answered(models.Model):
    aid = models.ForeignKey(Confirmer,on_delete=models.DO_NOTHING)
    sno = models.ForeignKey(Sentence,on_delete=models.CASCADE)

# Create your models here.

