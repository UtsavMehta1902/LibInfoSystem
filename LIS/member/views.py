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
            passnotmatch = True
            return render(request, "member/registration.html", {'passnotmatch':passnotmatch})

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
# function renders the main profile page of the user

@login_required(login_url = '/member/login')
def profile(request):

    user_name = request.user.username
    user_name = user_name.split("_")[0]
    is_faculty = False
    if(user_name == "FAC"):
        is_faculty = True
    
    issued_books = request.user.member.book_set.all()
    return render(request, "member/profile.html", {'is_faculty': is_faculty, 'issued_books':issued_books})

@login_required(login_url = '/member/login')
def view_current_issues(request):
    issued_books = request.user.member.book_set.all()
    reserved_book = request.user.member.reserved_book
    reserve_time = request.user.member.reserve_datetime

  
    issued_books = issued_books.exclude(issue_date=None)

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



@login_required(login_url = '/member/login')
def view_issue_history(request):
    issue_history = request.user.member.issuethread_set.all()
    issue_history = issue_history.order_by("-issue_date")
    return render(request, "member/view_issue_history.html", {'issue_history':issue_history})



@login_required(login_url = '/member/login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "member/view_books.html", {'books' :books})


def member_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is None:
            return render(request, "member/login.html", {'alert': "Invalid login credentials. Please try again."})

        member_type = username.split("_")[0]
        
        if member_type != "UG" and member_type != "PG" and member_type != "RS" and member_type != "FAC":
            alert = "The given username does not correspond to any member. Please enter a valid username."
            return render(request, "member/login.html", {'alert': alert})

        if user is not None:
            login(request, user)
         
            if request.user.is_superuser:
               
                return HttpResponse("The username or password entered by you is incorrect! Please enter correct member details!")
            else:
              
                return redirect("/member/profile")
        else:
         
            alert = "The given username does not correspond to any member. Please enter a valid username."
            return render(request, "member/login.html", {'alert':alert})
   
    return render(request, "member/login.html")


@login_required(login_url = '/member/login')
def profile(request):
    user_name = request.user.username
    user_name = user_name.split("_")[0]
    is_faculty = False
    if(user_name == "FAC"):
        is_faculty = True
    
    issued_books = request.user.member.book_set.all()
    return render(request, "member/profile.html", {'is_faculty': is_faculty, 'issued_books':issued_books})


def view_books(request):
    books = Book.objects.all()
    return render(request, "member/view_books.html", {'books' :books})



@login_required(login_url = '/member/login')
# @cache_control(no_cache=True, must_revalidate=True, no_store = True)
def issue_book(request, book_id):

    book = Book.objects.get(id=book_id)
    # print(request.user.id)
    member = request.user.member

    issued_books = member.book_set.all()
    if member.book_limit > len(issued_books):
        member.book_set.add(book)
        member.save()
        book.issue_date = datetime.date.today().isoformat()
        book.issue_member = member
        book.last_issue_date = datetime.date.today().isoformat()
        book.save()
        return render(request, "member/profile.html", {'alert':"The book has been issued to you!"})
    else:
        return render(request, "member/profile.html", {'alert':"You cannot issue this book currently. You have reached your maximum book issue limit!!"})

def reserve_book(request, book_id):
    book = Book.objects.get(id = book_id)
    member = request.user.member
    if(book.issue_member == member):
            return render(request, "member/profile.html", {'alert':"Cannot reserve this book for you, as this book is currently issued to you!"})

    if(member.reserved_book is not None): 
        if(member.reserved_book == book):
            return render(request, "member/profile.html", {'alert':"You have already reserved this book. You cannot reserve it again at present."})
        else: 
            return render(request, "member/profile.html", {'alert':"Cannot reserve this book for you. You already have a book currently reserved for you!"})
    else:
        member.reserved_book = book
        member.reserve_datetime = datetime.datetime.now()
        member.save()
        return render(request, "member/profile.html", {'alert':"You have been added to the waiting list for reserving this book. You will be notified if you have an active reservation on this book!"})


@login_required(login_url = '/member/login')
def view_issue_history(request):
    issue_history = request.user.member.issuethread_set.all()
    issue_history = issue_history.order_by("-issue_date")
    return render(request, "member/view_issue_history.html", {'issue_history':issue_history})


def return_book(request, book_id):

    book = Book.objects.get(id = book_id)
    book.return_requested = True
    book.save()
    return render(request, "member/profile.html", {'alert':"Your return request has been sent! Please wait for confirmation."})


def view_reminders(request):
    reminders = request.user.member.reminder_set.all()
    reminders = reminders.order_by("-rem_datetime")
    return render(request, "member/view_reminders.html", {'reminders': reminders})

def member_logout(request):
    logout(request)
    return redirect("/member/login")

