from django.test import TestCase
from book.models import Book
# Create your tests here.
import datetime


class TestBook(TestCase):

    print('PASS CASE: Trying Successful Book Creation: ')
    try:
        book = Book.objects.create(title="The Pilgrimage", author="Paulo Coelho",
                                       isbn="978-0-306-40355-7", rack_number="A2", date_added=datetime.date.today())
    except Exception as e:
        print(e)
    else:
        print('Test Passed')

    try:
        book = Book.objects.get(isbn = "978-0-306-40355-7")
        book.delete()

        book = Book.objects.get(isbn = "978-0-306-40355-7")
        print("Title of the book: ", book.title)

    except Exception as e:
        print("Exception: ", e)
        print("Book successfully deleted.")
