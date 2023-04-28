from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=60,blank=True)
    username= models.CharField(max_length=60,blank=True,unique=True)
    score = models.BigIntegerField(default=0)
    solved= models.BigIntegerField(default=0)
    password = models.TextField(max_length=200)
    email = models.CharField(max_length=70,blank=True)
    tag = models.IntegerField(default=0)
    about = models.CharField(max_length=200,blank=True)
    def _str_(self) -> str:
        t= str(self.id)+"  "+self.name
        return t

