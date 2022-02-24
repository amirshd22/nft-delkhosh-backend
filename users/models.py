from django.db import models
from django.contrib.auth.models import User
import uuid


class Userprofile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    number = models.CharField(max_length=12,null=True,blank=False)
    email = models.EmailField(null=True,blank=True)
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.number

