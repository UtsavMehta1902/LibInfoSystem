from django.test import TestCase
from staff.models import Staff
from django.contrib.auth.models import User
import datetime
# Create your tests here.


class TestStaff(TestCase):

        print('TEST CASE 1: ')
        # PASS TEST:
        try:   # the staff gets created as this user doesn't already exist in the database 
            user = User.objects.create_user(username="LIBC_20146", email="libc20146@gmail.com", password='pwd',first_name='staff', last_name='_1')
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

        print('\n\nTEST CASE 2:')
        # FAIL TEST:
        try:   # the user doesn't get created as this user's username is exactly same as that of the previous user, which is not allowed
            user = User.objects.create_user(username="LIBC_20146", email="libc20146@gmail.com", password='idk',first_name='staff', last_name='_1')
            clerk = Staff.objects.create(insti_id="20CS30037", user=user, book_limit=2, book_duration=1)
            user.save()
            clerk.save()

        except Exception as e:
            print('FAIL: New clerk creation failed')
            print(e)
            print("The clerk couldn't be created as there already exists a clerk with the same username.")
