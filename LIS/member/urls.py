from django.urls import path
from . import views

urlpatterns = [
    path("registration/", views.member_registration, name="member_registration"),
]