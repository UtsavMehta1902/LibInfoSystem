from django.urls import path
from . import views

urlpatterns = [
    path("registration/", views.member_registration, name="member_registration"),
    path("login/", views.member_login, name="member_login"),
    path("profile/", views.profile, name="profile"),
]