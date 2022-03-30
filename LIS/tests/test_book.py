from django.test import TestCase
from book.models import Book
# Create your tests here.
import datetime


class TestBook(TestCase):

    print('PASS CASE: Trying Successful Book Creation: ')
    try:
        book = Book.objects.create(title="The Alchemist", author="Paulo Coelho",
                                       isbn="978-0-306-40615-7", rack_number="A1", date_added=datetime.date.today())
    except Exception as e:
        print(e)
    else:
        print('Test Passed')
    
    print('FAIL CASE: Trying Unsuccessful Book Creation (Writing date in wrong format): ')
    try: 
        book = Book.objects.create(title="The Alchemist", author = "Paulo Coelho", isbn="978-0-306-40615-7", rack_number="A1", date_added="2019-29-3")
    except Exception as e:
        print(e)
    else:
        print('\nTest Passed')