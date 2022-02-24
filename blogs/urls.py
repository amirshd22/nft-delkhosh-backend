from django.urls import path
from . import views


urlpatterns = [
    path("", views.getBlogs, name="getBlogs"),
    path("blog/like/", views.create_like, name="createLike"),
]