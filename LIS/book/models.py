from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length= 15)
    rack_number = models.CharField(max_length= 10)
    issue_status = models.CharField(max_length= 15)
    date_issued = models.DateField(null=True)

   
    def __str__(self):
        return str(self.title) + " [ISBN: "+str(self.isbn)+']'
