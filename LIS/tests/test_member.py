from django.test import TestCase
from member.models import Member
from django.contrib.auth.models import User
import datetime
# Create your tests here.


class TestMember(TestCase):
        
        print('TEST CASE 1: UG')
        # PASS TEST:
        try:   # the user gets created as this user doesn't already exist in the database 
            user = User.objects.create_user(username="UG_20CS10095", email="nikhilgupta6@gmail.com", password='idk',first_name='nikhil', last_name='gupta')
            member = Member.objects.create(insti_id="20CS10095", user=user, book_limit=2, book_duration=1)
            user.save()
            member.save()
            print('PASS: New member created successfully!')
            print('Member details:')
            print('Full Name: ' + member.user.first_name + " " + member.user.last_name)
            print('Email: ' + member.user.email)
            print('Unique Institute ID:' +  member.insti_id)
            print('Username: ' + member.user.username)
            print('Book Limit: ', member.book_limit, " books")
            print('Allowed Issue duration: ', member.book_duration, " months")

        except Exception as e:
            print('FAIL: New member creation failed!')
            print(e)

        print('TEST CASE 2: UG')
        # FAIL TEST:
        try:   # the user doesn't get created as this user's username is exactly same as that of the previous user, which is not allowed
            user = User.objects.create_user(username="UG_20CS10093", email="nikhilgupta6@gmail.com", password='idk',first_name='nikhil', last_name='gupta')
            member = Member.objects.create(insti_id="20CS10093", user=user, book_limit=2, book_duration=1)
            user.save()
            member.save()
            print('PASS: New member created successfully!')
            print('Member details:')
            print('Full Name: ' + member.user.first_name + " " + member.user.last_name)
            print('Email: ' + member.user.email)
            print('Unique Institute ID:' + member.insti_id)
            print('Username: ' + member.user.username)
            print('Book Limit: ', member.book_limit, " books")
            print('Allowed Issue duration: ' , member.book_duration, " months")

        except Exception as e:
            print('FAIL: New member creation failed!')
            print(e)
            print("The member couldn't be created as there already exists a member with the same username.")


        print('TEST CASE 3: PG')
        # PASS TEST:
        try:   # the user gets created as this user doesn't already exist in the database 
            user = User.objects.create_user(username="PG_19CS40511", email="rakeshdwivedi@gmail.com", password='dwivedi$12321',first_name='Rakesh', last_name='Dwivedi')
            member = Member.objects.create(insti_id="19CS40511", user=user, book_limit=4, book_duration=1)
            user.save()
            member.save()
            print('PASS: New member created successfully!')
            print('Member details:')
            print('Full Name: ' + member.user.first_name + " " + member.user.last_name)
            print('Email: ' + member.user.email)
            print('Unique Institute ID:' + member.insti_id)
            print('Username: ' + member.user.username)
            print('Book Limit: ', member.book_limit, " books")
            print('Allowed Issue duration: ', member.book_duration, " months")

        except Exception as e:
            print('FAIL: New member creation failed!')
            print(e)

        print('TEST CASE 4: PG')
        # PASS TEST:
        try:   # the user gets created as this user doesn't exist in the database 
            user = User.objects.create_user(username="RS_20CD83R10", email="xyz@gmail.com", password='112358',first_name='nilesh', last_name='jain')
            member = Member.objects.create(insti_id="20CD83R10", user=user, book_limit=6, book_duration=3)
            user.save()
            member.save()
            print('PASS: New member created successfully!')
            print('Member details:')
            print('Full Name: ' + member.user.first_name + " " + member.user.last_name)
            print('Email: ' + member.user.email)
            print('Unique Institute ID:' + member.insti_id)
            print('Username: ' + member.user.username)
            print('Book Limit: ', member.book_limit, " books")
            print('Allowed Issue duration: ', member.book_duration, " months")

        except Exception as e:
            print('FAIL: New member creation failed!')
            print(e)


        print('TEST CASE 5: FACULTY')
        # PASS TEST:
        try:   # the user gets created as this user doesn't exist in the database 
            user = User.objects.create_user(username="FAC_DK_CS13937", email="faculty_name@cse.iitkgp.ac.in", password='iamfaculty',first_name='Donald', last_name='Knuth')
            member = Member.objects.create(insti_id="DK_CS13937", user=user, book_limit=10, book_duration=6)
            user.save()
            member.save()
            print('PASS: New member created successfully!')
            print('Member details:')
            print('Full Name: ' + member.user.first_name + " " + member.user.last_name)
            print('Email: ' + member.user.email)
            print('Unique Institute ID:' + member.insti_id)
            print('Username: ' +  member.user.username)
            print('Book Limit: ' ,member.book_limit, " books")
            print('Allowed Issue duration: ', member.book_duration, " months")

        except Exception as e:
            print('FAIL: New member creation failed!')
            print(e)
        
        
        