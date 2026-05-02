from django.db import models

# Create your models here.
class UserSignup(models.Model):
    fullname=models.CharField(max_length=20)
    email=models.EmailField()
    mobile=models.BigIntegerField()
    city=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    cpassword=models.CharField(max_length=20)