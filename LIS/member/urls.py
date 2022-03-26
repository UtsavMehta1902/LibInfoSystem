from django.urls import path
from . import views

urlpatterns = [
    path("registration/", views.member_registration, name="registration"),
    path("login/", views.member_login, name="member_login"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.member_logout, name="logout"),
    path('', views.member_home_page, name="home"),
]