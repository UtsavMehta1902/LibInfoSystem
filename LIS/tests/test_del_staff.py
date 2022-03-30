from django.test import TestCase
from staff.models import Staff
from django.contrib.auth.models import User
import datetime
# Create your tests here.


class TestStaff(TestCase):


    print('TEST CASE 1: ')
    # PASS TEST:
    try:   # the staff gets created as this user doesn't already exist in the database 
        user = User.objects.create_user(username="LIBC_20PK123", email="libc20PK123@gmail.com", password='kdi',first_name='pawan', last_name='kumar')
        clerk = Staff.objects.create(user=user)
        user.save()
        clerk.save()
        print('PASS: New clerk created successfully')
        print('Clerk details:')
        print('Full Name: ' + clerk.user.first_name + " " + clerk.user.last_name)
        print('Email: ' + clerk.user.email)
        print('Username: ' + clerk.user.username)

    except Exception as e:
        print('FAIL: New clerk creation failed')
        print(e)

    print('TEST Deletion')
   
    try:
        user = User.objects.get(username="LIBC_20PK123")
        user.delete()
   
        user = User.objects.get(username="LIBC_20PK123")
        print(user.first_name)

    except Exception as e:
        print(e)
        print('User deleted successfully')
    
    
