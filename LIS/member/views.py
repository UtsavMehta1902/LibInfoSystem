
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
import datetime
# from django.conf import settings
# from django.core.mail import send_mail

def member_home_page(request):
    return render(request, "member/home.html")

def member_registration(request):
    if request.method == "POST":

        member_type = request.POST['member_type']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        insti_id = request.POST['insti_id']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        username = ""
        limit=0
        duration=0

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

        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        member = Member.objects.create(insti_id=insti_id, user=user, book_limit=limit, book_duration=duration)
        
        user.save()
        member.save()

        # subject = "Welcome to the Library"
        # message = f"Hello {first_name + last_name}!\nThank you for registering to our LIS portal.\nYour username is {username}.\nPlease login to your account to continue."
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [email,]
        # send_mail( subject, message, email_from, recipient_list, fail_silently=False)
        message = f"Your username is {username}. Please remember this for future purposes."
        return render(request, 'member/login.html', {'message': message})
        return render(request, "member/registration.html")  
    return render(request, "member/registration.html")

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

def member_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a Member!!")
            else:
                return redirect("/member/profile")
        else:
            alert = True
            return render(request, "member/login.html", {'alert':alert})
    return render(request, "member/login.html")

def member_logout(request):
    logout(request)
    return redirect("/member/login")

def issue_book(request, book_id):
    book = Book.objects.get(id=book_id)
    member = request.user.member

    issued_books = member.book_set.all()
    if member.book_limit > len(issued_books):
        member.book_set.add(book)
        member.save()
        book.issue_date = datetime.date.today().isoformat()
        book.issue_member = member
        book.save()
        return render(request, "member/profile.html", {'alert':"Issue Request Sent, Please wait for email confirmation."})
    else:
        return render(request, "member/profile.html", {'alert':"You cannot issue this book currently. You have reached your maximum book issue limit!!"})

def reserve_book(request, book_id):
    book = Book.objects.get(id = book_id)
    member = request.user.member

    if(member.reserved_book != None):
        return render(request, "member/profile.html", {'alert':"Cannot reserve this book for you. You already have a book currently reserved for you!"})
    else:
        member.reserved_book = book
        member.reserve_datetime = datetime.datetime.now()
        member.save()
        return render(request, "member/profile.html", {'alert':"You have been added to the waiting list for reserving this book. You will be notified if you have an active reservation on this book!"})
