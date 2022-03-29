from django.urls import path
from . import views

urlpatterns = [

    #  if a member tries to access a webpage associated with a staff member, or vice-versa, the user would be directed
    #  to the 403 page, displaying unauthorised access
    path('403/', views.error_403, name='error_403'),

    # this url is for the home page of our Library Information System 
    path('', views.home_page, name='home'),
]