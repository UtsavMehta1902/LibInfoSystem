from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect,render,HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.sites.shortcuts import get_current_site
from dateutil.relativedelta import relativedelta


# function to register a member
def member_registration(request):

    # post method is called when a new member registers through the registration form
    if request.method == "POST":

        member_type = request.POST.get('member_type', "")
        first_name = request.POST.get('first_name',"")
        last_name = request.POST.get('last_name',"")
        email = request.POST.get('email',"")
        insti_id = request.POST.get('insti_id',"")
        password = request.POST.get('password',"")
        confirm_password = request.POST.get('confirm_password',"")
        
        username = ""
        limit=0
        duration=0

        # username of a member is : member_type + str(insti_id)

        if member_type == "UG":
            username= "UG_" + str(insti_id)
            limit=2
            duration=1
        elif member_type == "PG":
            username= "PG_" + str(insti_id)
            limit=4
            duration=1
        elif member_type == "RS":
            username= "RS_" + str(insti_id)
            limit=6
            duration=3
        elif member_type == "FAC":
            username= "FAC_" + str(insti_id)
            limit=10
            duration=6

        
        if password != confirm_password:
            return render(request, "member/registration.html", {'message':"Passwords do not match. Please try again."})

        if Member.objects.filter(insti_id=insti_id).exists():
            return render(request, "member/registration.html", {'message':"The given username already exists. Please try again."})
            
        # creating a new object of the member class
        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        member = Member.objects.create(insti_id=insti_id, user=user, book_limit=limit, book_duration=duration)
        
        # saving the object created to the Django database
        user.save()
        member.save()

        # the following message prompt will be shown on screen on successful registration,
        # showing the username to the member for future login
        message = f"Registration Completed Successfully! Your username is {username}. Please remember this for future purposes."
    
        return render(request, "member/registration.html", {'message': message})

    return render(request, "member/registration.html")



# this function is only accessible to a member and not to a staff member as it requires member login

@login_required(login_url = '/member/login')
def profile(request):

    # function renders the main profile page of the user

    user_name = request.user.username
    user_name = user_name.split("_")[0]
    is_faculty = False

    # this loop conditions whether the user is a faculty or not and shows his faculty id if he is a faculty, else shows the member roll number 
    if(user_name == "FAC"):
        is_faculty = True
    
    return render(request, "member/profile.html", {'is_faculty': is_faculty})



# this function is only accessible to a member and not to a staff member as it requires member login
@login_required(login_url = '/member/login')
def view_current_issues(request):
    # function to show a member what all books are currently issued by him and what book is currently reserved by him

    issued_books = request.user.member.book_set.all()
    reserved_book = request.user.member.reserved_book
    reserve_time = request.user.member.reserve_datetime
    issued_books = issued_books.exclude(issue_date=None)

    # to show the due date of the currently issued books to the member
    due_dates = []
    for book in issued_books:
        due_dates.append(book.issue_date + relativedelta(months=book.issue_member.book_duration))

    book_details = zip(issued_books, due_dates)

    try:
        active_member = reserved_book.member_set.all().order_by('reserve_datetime').first()
    except(Exception):
        active_member = None
    
    if reserved_book is not None: 
        if (active_member and active_member.user.username == request.user.username):
            reservation_status = "Active"
        else:
            reservation_status ="Pending"
    else:
        reservation_status = "Not Applicable"
    return render(request, "member/view_issued_books.html", {'total_books': len(issued_books), 'reserved_book': reserved_book, 'reserve_time': reserve_time, 'reservation_status': reservation_status, 'book_details':book_details})


# this function is only accessible to a member and not to a staff member as it requires member login
@login_required(login_url = '/member/login')
def view_issue_history(request):
    # function to show the entire issue history to a member , where the issues are sorted according to latest first
    # a book issued by a member is shown in issue history only if it was returned by the member

    issue_history = request.user.member.issuethread_set.all()
    issue_history = issue_history.order_by("-issue_date")
    return render(request, "member/view_issue_history.html", {'issue_history':issue_history})


# this function is only accessible to a member and not to a staff member as it requires member login
@login_required(login_url = '/member/login')
def view_books(request):
    # function to show all the books present in the Library for the user to issue/reserve books

    books = Book.objects.all()
    return render(request, "member/view_books.html", {'books' :books})


def member_login(request):

    # user enters his/her credentials in the Login form
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        # if there doesn't exist a user corresponding to the entered username
        if user is None:
            return render(request, "member/login.html", {'alert': "Invalid login credentials. Please try again."})

        # member_type check is necessary so that a Librarian or Clerk cannot login from this page
        member_type = username.split("_")[0]
        if member_type != "UG" and member_type != "PG" and member_type != "RS" and member_type != "FAC":
            alert = "The given username does not correspond to any member. Please enter a valid username."
            return render(request, "member/login.html", {'alert': alert})
        
        # if the username matched with the database
        if user is not None:
            login(request, user)
            
            # to prevent superuser from login
            if request.user.is_superuser:
                return HttpResponse("The username or password entered by you is incorrect! Please enter correct member details!")
            
            else:  
                return redirect("/member/profile")

        else:  
            alert = "The given username does not correspond to any member. Please enter a valid username."
            return render(request, "member/login.html", {'alert':alert})
   
    return render(request, "member/login.html")


# this function is only accessible to a member and not to a staff member as it requires member login
@login_required(login_url = '/member/login')
def issue_book(request, book_id):


    book = Book.objects.get(id=book_id)   #book to be issued
    member = request.user.member          # member who wants to issue the book

    issued_books = member.book_set.all()

    # if the member hasn't exceeded his max issue limit at a time, book is issued to him
    if member.book_limit > len(issued_books):
        member.book_set.add(book)
        book.issue_date = datetime.date.today().isoformat()
        book.issue_member = member
        book.last_issue_date = datetime.date.today().isoformat()
        if member.reserved_book == book :
            member.reserved_book = None
            member.reserve_datetime = None
        book.save()
        member.save()
        return render(request, "member/profile.html", {'alert':"The book has been issued to you!"})

    # if the member has already issued the max number of books he can at a time
    else:
        return render(request, "member/profile.html", {'alert':"You cannot issue this book currently. You have reached your maximum book issue limit!!"})


# this function is only accessible to a member and not to a staff member as it requires member login
@login_required(login_url = '/member/login')
def reserve_book(request, book_id):

    book = Book.objects.get(id = book_id)
    member = request.user.member

    # if the book which the member wants to reserve is currently issued to him, the reservation is declined
    if(book.issue_member == member):
            return render(request, "member/profile.html", {'alert':"Cannot reserve this book for you, as this book is currently issued to you!"})

    # if the member has already reserved a book at present
    if(member.reserved_book is not None): 

        # if the book which the user wants to reserve is already currently reserved by him (to prevent repeated reserve request)
        if(member.reserved_book == book):
            return render(request, "member/profile.html", {'alert':"You have already reserved this book. You cannot reserve it again at present."})
        else: 
            return render(request, "member/profile.html", {'alert':"Cannot reserve this book for you. You already have a book currently reserved for you!"})
    
    else:
        member.reserved_book = book
        member.reserve_datetime = datetime.datetime.now()
        member.save()
        return render(request, "member/profile.html", {'alert':"You have been added to the waiting list for reserving this book. You will be notified if you have an active reservation on this book!"})


# this function is only accessible to a member and not to a staff member as it requires member login
@login_required(login_url = '/member/login')
def return_book(request, book_id):

    # function to send a return request for a book to the portal, which would be approved by a clerk
    book = Book.objects.get(id = book_id)
    book.return_requested = True
    book.save()
    return render(request, "member/profile.html", {'alert':"Your return request has been sent! Please wait for confirmation."})


# this function is only accessible to a member and not to a staff member as it requires member login
@login_required(login_url = '/member/login')
def view_reminders(request):

    # function allows a member to view the notifications or reminders sent to him
    reminders = request.user.member.reminder_set.all()
    reminders = reminders.order_by("-rem_datetime")
    return render(request, "member/view_reminders.html", {'reminders': reminders})


# function called when member presses on logout from the member's navigation bar
def member_logout(request):
    logout(request)
    return redirect("/member/login")
