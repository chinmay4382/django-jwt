from django.db import models


# Create your models here.

class UserDetailModel(models.Model):
    user_id = models.AutoField(primary_key=True,auto_created=True)
    first_name = models.CharField(max_length=100,blank=False)
    last_name = models.CharField(max_length=100,blank =False)
    email = models.EmailField(blank=False,unique=True)
    phone = models.CharField(blank=False,unique=True,max_length=10)
    password = models.CharField(max_length=128,blank=False,  unique=True,)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=True)