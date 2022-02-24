from django.urls import path
from . import views



urlpatterns = [
    path("login/", views.MyTokenObtainPairView.as_view(), name="login"),
    path("register/",views.RegisterView.as_view(), name="register"),
    path("profile/", views.getProfile, name="profile"),
    path("profile/edit/", views.editProfile, name="editProfile"),
    path("profile/delete/", views.deleteUser, name="deleteProfile"),
]