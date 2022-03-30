from django.test import TestCase
from book.models import Book
# Create your tests here.
import datetime

class TestBook(TestCase):
    
    def test_create_book_success(self):
        print('Trying Successful Book Creation: ')
        try:
            book = Book.objects.create(title="The Alchemist", author="Paulo Coelho", isbn="978-0-306-40615-7", rack_number="A1", date_added=datetime.date.today())
        except Exception as e:
            print(e)
        else:
            print('Test Passed')
    
    def test_create_book_fail(self):
        print('Trying Unsuccessful Book Creation: ')
        try:
            book = Book.objects.create(title="The Alchemist", author = "Paulo Coelho", isbn="978-0-306-40615-7", rack_number="A1", date_added="2019-29-3")
        except Exception as e:
            print(e)
        else:
            print('\nTest Passed')