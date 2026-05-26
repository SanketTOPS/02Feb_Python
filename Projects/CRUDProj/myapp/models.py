from django.db import models

# Create your models here.
class Userinfo(models.Model):
    fullname=models.CharField(max_length=50)
    email=models.EmailField()
    dob=models.DateField()
    mobile=models.BigIntegerField()