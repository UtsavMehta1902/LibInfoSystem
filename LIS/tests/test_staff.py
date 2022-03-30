from django.test import TestCase
from staff.models import Staff
from django.contrib.auth.models import User
import datetime
# Create your tests here.


class TestStaff(TestCase):

        print('TEST CASE 1: ')
        # PASS TEST:
        try:   # the staff gets created as this user doesn't already exist in the database 
            user = User.objects.create_user(username="LIBC_20256", email="libc20256@gmail.com", password='pwd',first_name='staff', last_name='_1')
            clerk = Member.objects.create(user=user)
            print('PASS: New clerk created successfully')
            print('Clerk details:')
            print('Full Name: ' + clerk.first_name + " " + clerk.last_name)
            print('Email: ' + clerk.email)
            print('Unique Institute ID:' clerk.insti_id)
            print('Username: ' clerk.user.username)
            print('Book Limit: ' + clerk.book_limit + " books")
            print('Allowed Issue duration: ' + clerk.book_duration + " months")

        except Exception as e:
            print('FAIL: New clerk creation failed')
            print(e)

        print('TEST CASE 2:')
        # FAIL TEST:
        try:   # the user doesn't get created as this user's username is exactly same as that of the previous user, which is not allowed
            user = User.objects.create_user(username="UG_20CS30037", email="nyatipranav26@gmail.com", password='idk',first_name='Pranav', last_name='Nyati')
            clerk = Staff.objects.create(insti_id="20CS30037", user=user, book_limit=2, book_duration=1)
            print('PASS: New clerk created successfully')
            print('clerk details:')
            print('Full Name: ' + clerk.first_name + " " + clerk.last_name)
            print('Email: ' + clerk.email)
            print('Unique Institute ID:' clerk.insti_id)
            print('Username: ' clerk.user.username)
            print('Book Limit: ' + clerk.book_limit + " books")
            print('Allowed Issue duration: ' + clerk.book_duration + " months")

        except Exception as e:
            print('FAIL: New clerk creation failed')
            print(e)
            print("The clerk couldn't be created as there already exists a clerk with the same username.")


        print('TEST CASE 3:')
        # PASS TEST:
        try:   # the user gets created as this user doesn't already exist in the database 
            user = User.objects.create_user(username="PG_20CS40012", email="rakeshsharma@gmail.com", password='sharma$12321',first_name='Rakesh', last_name='Sharma')
            clerk = Staff.objects.create(insti_id="20CS40012", user=user, book_limit=4, book_duration=1)
            print('PASS: New clerk created successfully')
            print('clerk details:')
            print('Full Name: ' + clerk.first_name + " " + clerk.last_name)
            print('Email: ' + clerk.email)
            print('Unique Institute ID:' clerk.insti_id)
            print('Username: ' clerk.user.username)
            print('Book Limit: ' + clerk.book_limit + " books")
            print('Allowed Issue duration: ' + clerk.book_duration + " months")

        except Exception as e:
            print('FAIL: New clerk creation failed')
            print(e)

        print('TEST CASE 4:')
        # PASS TEST:
        try:   # the user gets created as this user doesn't exist in the database 
            user = User.objects.create_user(username="RS_20CD92R01", email="xyz@gmail.com", password='idk',first_name='Pranav', last_name='Nyati')
            clerk = Staff.objects.create(insti_id="20CS30037", user=user, book_limit=2, book_duration=1)
            print('PASS: New clerk created successfully')
            print('clerk details:')
            print('Full Name: ' + clerk.first_name + " " + clerk.last_name)
            print('Email: ' + clerk.email)
            print('Unique Institute ID:' clerk.insti_id)
            print('Username: ' clerk.user.username)
            print('Book Limit: ' + clerk.book_limit + " books")
            print('Allowed Issue duration: ' + clerk.book_duration + " months")

        except Exception as e:
            print('FAIL: New clerk creation failed')
            print(e)


        print('TEST CASE 5:')
        # PASS TEST:
        try:   # the user gets created as this user doesn't exist in the database 
            user = User.objects.create_user(username="UG_20CS30037", email="nyatipranav26@gmail.com", password='idk',first_name='Pranav', last_name='Nyati')
            clerk = Staff.objects.create(insti_id="20CS30037", user=user, book_limit=2, book_duration=1)
            print('PASS: New clerk created successfully')
            print('clerk details:')
            print('Full Name: ' + clerk.first_name + " " + clerk.last_name)
            print('Email: ' + clerk.email)
            print('Unique Institute ID:' clerk.insti_id)
            print('Username: ' clerk.user.username)
            print('Book Limit: ' + clerk.book_limit + " books")
            print('Allowed Issue duration: ' + clerk.book_duration + " months")

        except Exception as e:
            print('FAIL: New clerk creation failed')
            print(e)