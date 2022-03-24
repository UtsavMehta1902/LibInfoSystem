from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    book_limit = models.IntegerField()
    book_duration = models.IntegerField()
    # reserved_books = models.ForeignKey(Book,on_delete=models.CASCADE, null=True, default=None)
    reminder = models.CharField(max_length=300, blank=True, default='')
    # issued_books = models.ManyToManyField(Book, related_name='issued_books', blank=True, default=None)

    def __str__(self):
        return str(self.user)

