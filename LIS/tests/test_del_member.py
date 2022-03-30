from django.test import TestCase
from member.models import Member
from django.contrib.auth.models import User
import datetime
# Create your tests here.


class TestMember(TestCase):
        
    print('Creating a Member object')
        # PASS TEST:
    try:   # the user gets created as this user doesn't already exist in the database 
        user = User.objects.create_user(username="UG_20CS10040", email="nikhilgupta6@gmail.com", password='idk',first_name='nikhil', last_name='gupta')
        member = Member.objects.create(insti_id="20CS10040", user=user, book_limit=2, book_duration=1)
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

    print('TEST Deletion')
    
    try:
        member = Member.objects.get(insti_id="20CS10040")
        user.delete()
        member.delete()

        print(member.user.first_name)

    except Exception as e:
        print(e)
