from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/blogs/", include("blogs.urls")),
    path("api/advertising/", include("advertising.urls")),
    path("api/consulting/", include("Consulting.urls")),
    path("api/courses/", include("courses.urls")),
    path("api/nft/",include("nft.urls"))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

