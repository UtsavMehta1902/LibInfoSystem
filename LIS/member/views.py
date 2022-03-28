from operator import truediv
import re
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
import datetime
# from django.core.mail import EmailMessage
from django.conf import settings
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
# import json

# from django.core.mail.backends.smtp import EmailMessage, EmailBackend
# Create your views here.
# UG_cnt=0
# PG_cnt=0
# RS_cnt=0
# FAC_cnt=0

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
        
        # user.is_active = False
        user.save()
        member.save()

        # connection = EmailBackend(host='smtp.gmail.com',
        # port=587,
        # username='noreplycomposit2022@gmail.com', 
        # password='composit@2022')
        
    
        # body = render_to_string('email_verification.html', {
        # 'user': user,
        # 'domain': 'composit-api.herokuapp.com',
        # # 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        # 'token': account_activation_token.make_token(user),
        # })

        # emailSender = EmailMessage(
        #     'Composit Registration confirmed',
        #     body,
        #     settings.EMAIL_HOST_USER,
        #     [email],
        #     bcc=['sailokesh.gorantla@ecell-iitkgp.org'],
        #     connection=connection
        # )
        # emailSender.fail_silently = False
        # emailSender.send()


        return redirect('/member/login')
        return render(request, "member/registration.html", {'alert':alert})
    return render(request, "member/registration.html")

# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         # return redirect('home')
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')

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
    return render(request, "member/view_issued_books.html", {'issued_books':issued_books, 'reserved_book': reserved_book})


def view_books(request):
    books = Book.objects.all()
    return render(request, "member/view_books.html", {'books' :books})

def member_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        member_type = username.split("_")[0]
        
        if member_type != "UG" and member_type != "PG" and member_type != "RS" and member_type != "FAC":
            # alert = True
            return render(request, "member/login.html", {'alert': "The given username does not correspond to any member. Please enter a valid username."})

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("The username or password entered by you is incorrect! Please enter correct member details!")
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
