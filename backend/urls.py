from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/blogs/", include("blogs.urls")),
    path("api/advertising/", include("advertising.urls")),
    path("api/consulting/", include("Consulting.urls")),
    path("api/courses/", include("courses.urls")),
]