from django.db import models
from django.contrib.auth.models import User
from book.models import Book



# Member class: 
# An object of the member class represents a unique member on the Library Information Portal

# Member class has the following attributes:
# -> user: is the default Django user
# -> book limit: each user has a book issue limit based on whether he/she is a UG, PG, RS, and Faculty
# -> insti_id: refers to the unique id for a user: Roll Number for a student, and unique Faculty ID for a faculty
# -> book_duration: refers to the maximum duration for which a book can be issued to a member, without incurring penalty
# -> reserved_book: maps to a book which is currently reserved by the member, and if the member has no reservation, it stores None
# -> reserve_datetime: stores the date and time when reservation for a book was made
# -> issue_history: 

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    book_limit = models.IntegerField()
    insti_id = models.CharField(max_length=15, null = True, default= None)
    book_duration = models.IntegerField()
    reserved_book = models.ForeignKey(Book,on_delete=models.SET_NULL, null=True, default=None)
    reserve_datetime = models.DateTimeField(null = True)
    # issue_history = models.CharField(max_length = 500, null = True)

    def __str__(self):
        return str(self.user)

# Reminder class: 
# An instance of the reminder class (it is basically a helper class) is generated when a reminder is sent to a member by the Librarian

# Reminder class has the following attributes:
# -> rem_id: stores the info of the type of reminder -> whether it is an overdue reminder, or an active reservation reminder
# -> message: body(text) of the reminder/notification that will be displayed to the member in his reminders inbox
# -> penalty: stores the amount of penalty fee if the reminder is related to an overdue book
# -> book: maps to the book regarding which the reminder is being sent
# -> member: maps to the member to whom the reminder is being sent
# -> rem_datetime: stores the date and time when the Librarian sent a reminder to the member

class Reminder(models.Model):
    rem_id = models.CharField(max_length = 10)
    message = models.CharField(max_length = 200)
    penalty = models.FloatField(default = 0.0)
    book  = models.ForeignKey(Book, on_delete = models.CASCADE)
    member = models.ForeignKey(Member, on_delete = models.CASCADE)
    rem_datetime = models.DateTimeField(null = True)


# IssueThread class: 
# this is basically a helper class, and an instance of it refers to a complete issue and return process for a member
# the class is useful in storing the complete issue history of a member and display it on his profile

# attributes of this class are:
# -> member: matches to the member who issued a particular book
# -> book: refers to the book which was issued by the member
# -> issue_date: refers to the date on which the member issued the book
# -> return_date: refers to the date on which the member returned the book
# -> penalty: if the bbok was returned later than its due date, the penalty that was incurred will also be shown to the user

class IssueThread(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book  = models.ForeignKey(Book, on_delete = models.CASCADE)
    issue_date = models.DateField(null= True)
    return_date = models.DateField(null= True)
    penalty = models.FloatField(default= 0.0)
