from django.db import models
from django.contrib.auth.models import User
import uuid

class Blog(models.Model):
    title= models.CharField(max_length=255,null=True,blank=False)
    description= models.TextField(null=True, blank=True)
    image= models.ImageField(upload_to="images/",null=True)
    id= models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    likes_count= models.IntegerField(default=0,null=True,blank=False)
    createdAt= models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.title

class Like(models.Model):
    user= models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    blog= models.ForeignKey(Blog,on_delete=models.CASCADE,null=True,related_name="blog")
    id= models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.user.username

