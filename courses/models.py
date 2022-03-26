from hashlib import blake2b
from django.db import models
from django.contrib.auth.models import User
import uuid


class Course(models.Model):
    title = models.CharField(max_length=255,null=True,blank=False)
    thumbnail = models.ImageField(upload_to="images/",null=True,blank=True)
    file = models.FileField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    price = models.IntegerField(null=True,blank=False)
    students = models.IntegerField(default=0,null=True,blank=True)
    createdAt= models.DateTimeField(auto_now_add=True,null=True)
    available = models.BooleanField(default=False,null=True,blank=False)
    id= models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

class CourseReview(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True,related_name="review_course")
    rate= models.IntegerField(default=0, null=True,blank=True)
    content= models.CharField(max_length=255,null=True,blank=False)
    id= models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.user.username

class OrderCourses(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True,related_name="order_course")
    isPaid= models.BooleanField(default=False, null=True,blank=False)
    paidAt= models.DateTimeField(null=True, blank=True)
    transId= models.CharField(max_length=255, null=True,blank=True)
    createdAt= models.DateTimeField(auto_now_add=True,null=True)
    url = models.CharField(max_length=255,null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.user.username



class OwnedCourse(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True,related_name="owned_course")
    createdAt= models.DateTimeField(auto_now_add=True,null=True)
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.user.username