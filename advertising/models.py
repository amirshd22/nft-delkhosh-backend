from django.db import models
from django.contrib.auth.models import User
import uuid

class AdvertisingPlan(models.Model):
    title= models.CharField(max_length=255,null=True,blank=False)
    description= models.TextField(null=True,blank=True)
    price= models.IntegerField(default=0,null=True,blank=False)
    createdAt= models.DateTimeField(auto_now_add=True,null=True)
    people_used= models.IntegerField(default=0,null=True,blank=True)
    id= models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title



class OrderAdvertising(models.Model):
    user= models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    plan= models.ForeignKey(AdvertisingPlan, on_delete=models.SET_NULL, null=True,related_name="order_advertising")
    image= models.ImageField(upload_to="images/", null=True,blank=True)
    link= models.TextField(null=True,blank=False)
    description= models.TextField(null=True,blank=True)
    isPaid= models.BooleanField(default=False, null=True,blank=False)
    paidAt= models.DateTimeField(null=True, blank=True)
    transId= models.CharField(max_length=255, null=True,blank=True)
    createdAt= models.DateTimeField(auto_now_add=True,null=True)
    isLive= models.BooleanField(default=False,null=True,blank=False)
    id= models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    url = models.CharField(max_length=355, null=True,blank=True)

    def __str__(self):
        return f"{self.user.username}-{self.transId}-{self.isPaid}"
