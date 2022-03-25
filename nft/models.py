from django.db import models
import uuid
from django.contrib.auth.models import User

class NftPlan(models.Model):
    title = models.CharField(max_length=255, null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    more_details = models.TextField(null=True,blank=True)
    price = models.IntegerField(default=0,null=True,blank=False)
    id= models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    available = models.BooleanField(default=False,null=True,blank=False)
    url = models.CharField(max_length=255, null=True,blank=True)
    createdAt= models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.title



class Order(models.Model):
    plan = models.ForeignKey(NftPlan, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    description = models.TextField(null=True,blank=True)
    id= models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    createdAt= models.DateTimeField(auto_now_add=True,null=True)
    isPaid = models.BooleanField(default=False,null=True,blank=False)
    createdAt= models.DateTimeField(auto_now_add=False,null=True, blank=True)
    details = models.TextField(null=True,blank=True)
    transId = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return f"{self.user.username}-{self.transId}-{self.isPaid}"    


