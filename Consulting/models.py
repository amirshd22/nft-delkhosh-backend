import re
from django.db import models
from django.contrib.auth.models import User
import uuid


class ConsultingPlan(models.Model):
    title = models.CharField(max_length=255,null=True,blank=False)
    description = models.TextField(null=True,blank=True)
    price = models.IntegerField(default=0,null=True,blank=False)
    people_used = models.IntegerField(default=0,null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True,null=True)
    available = models.BooleanField(default=False,null=True,blank=False)
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    

class OrderConsulting(models.Model):
    user= models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    plan= models.ForeignKey(ConsultingPlan, on_delete=models.SET_NULL, null=True,related_name="order_consulting")
    isPaid= models.BooleanField(default=False, null=True,blank=False)
    paidAt= models.DateTimeField(null=True, blank=True)
    description= models.TextField(null=True,blank=True)
    transId= models.CharField(max_length=255, null=True,blank=True)
    createdAt= models.DateTimeField(auto_now_add=True,null=True)
    consulting_time = models.CharField(max_length=255, null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)


    def __str__(self):
        return self.user.username