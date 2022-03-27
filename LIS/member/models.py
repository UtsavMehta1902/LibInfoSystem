from django.db import models
from django.contrib.auth.models import User
from book.models import Book

# Create your models here.

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    book_limit = models.IntegerField()
    insti_id = models.CharField(max_length=15, null = True, default= None)
    book_duration = models.IntegerField()
    reserved_book = models.ForeignKey(Book,on_delete=models.SET_NULL, null=True, default=None)
    # reminder = models.CharField(max_length=300, blank=True, default='')
    # issued_books = models.ManyToManyField(Book, related_name='issued_books', blank=True, default=None)
    reserve_datetime = models.DateTimeField(null = True)
    issue_history = models.CharField(max_length = 500, null = True)


    def __str__(self):
        return str(self.user)

# class Reservation(models.Model):
#     member = models.OnetoOneField(Member, on_delete = models.CASCADE)
#     reserve_date = models.DateField(null = True)
#     book = models.ForeignKey(Book, on_delete = models.CASCADE)


class Reminder(models.Model):
    rem_id = models.CharField(max_length = 10)
    message = models.CharField(max_length = 200)
    penalty = models.FloatField(default = 0.0)
    book  = models.OneToOneField(Book, on_delete = models.CASCADE)
    member = models.ForeignKey(Member, on_delete = models.CASCADE)
    date_of_rem = models.DateField(null = True)

    