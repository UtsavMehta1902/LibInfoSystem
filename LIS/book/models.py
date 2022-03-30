from django.db import models
# from member.models import Member

# Create your models here.


# Book model has the following attributes:
# -> title: title of book, author: names of the authors of the book
# -> ISBN: unique international book number to recognise a book
# -> rack_number -> string storing the rack number where the user can search for this book
# -> issue_date -> if the book is currently issued to someone, it will store when it was issued to the user, else it will store the empty string
# -> date_added -> stores the date on which the book was added to the library portal by the librarian
# -> return requested -> if the return for this book is requested by a member and is waiting for a clerk's approval
# -> issue_member -> links to the member who has issued the book at present, else it stores NULL
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length= 20)
    rack_number = models.CharField(max_length= 10)
    issue_date = models.DateField(null= True)
    date_added = models.DateField(null=True)
    return_requested = models.BooleanField(default=False)
    last_issued_date = models.DateField(null=True)
    # #field visible only to the clerks and librarian in book display
    issue_member = models.ForeignKey("member.Member", on_delete = models.SET_NULL, null = True)
    active_reserve_date = models.DateField(null=True, default=None)
    active_reserve_by = models.CharField(max_length=200, default="")
    
    def __str__(self):
        return str(self.title) + " [ISBN: "+str(self.isbn)+']'
