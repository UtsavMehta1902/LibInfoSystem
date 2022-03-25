from django.db import models
from django.contrib.auth.models import User
from book.models import Book
# Create your models here.

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
