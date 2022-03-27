from django.db import models
# from member.models import Member

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length= 15)
    rack_number = models.CharField(max_length= 10)
    issue_date = models.DateField(null= True)
    date_added = models.DateField(null=True)
    
    # #field visible only to the clerks and librarian in book display
    issue_member = models.ForeignKey("member.Member", on_delete = models.SET_NULL, null = True)

   
    def __str__(self):
        return str(self.title) + " [ISBN: "+str(self.isbn)+']'




