from django.db import models
from django.contrib.auth.models import User
from book.models import Book
# Create your models here.


# Staff class:
# the Staff class models all the clerks and the Librarian of the Library, implemented using the Django user 
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
