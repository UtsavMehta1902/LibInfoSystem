from django.urls import path
from . import views

urlpatterns = [
    path('403/', views.error_403, name='error_403'),
    path('', views.home_page, name='home'),
]