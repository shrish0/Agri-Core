from django.db import models
# from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    usertype=models.CharField( max_length=50,default="farmer")
    phone=models.CharField(max_length=10)
