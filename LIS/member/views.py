from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect,render,HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
import datetime
from django.core.mail import EmailMessage
from django.conf import settings
import pytz
from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
import json
from django.views.decorators.cache import cache_control
#from django.core.mail.backends.smtp import EmailMessage, EmailBackend
# Create your views here.
# UG_cnt=0
# PG_cnt=0
# RS_cnt=0
# FAC_cnt=0


def member_home_page(request):
    return render(request, "member/home.html")


def member_registration(request):
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
        message = f"Registration Completed Successfully! Your username is {username}. Please remember this for future purposes."
        return render(request, "member/registration.html", {'message': message})
    return render(request, "member/registration.html")

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



@cache_control(no_cache=True, must_revalidate=True, no_store = True)
def member_login(request):
    # prev_page_path = request.META['HTTP_REFERER']
    # prev_page_path = prev_page_path.split("next=")[-1]
    # print(prev_page_path)
    # if(prev_page_path == "/member/profile/"):


    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        member_type = username.split("_")[0]
        
        if member_type != "UG" and member_type != "PG" and member_type != "RS" and member_type != "FAC":
            alert = "The given username does not correspond to any member. Please enter a valid username."
            return render(request, "member/login.html", {'alert': alert})

        if user is not None:
            login(request, user)
            print('a')
            if request.user.is_superuser:
                print('b')
                return HttpResponse("The username or password entered by you is incorrect! Please enter correct member details!")
            else:
                print('c')
                return redirect("/member/profile")
        else:
            print('d')
            alert = "The given username does not correspond to any member. Please enter a valid username."
            return render(request, "member/login.html", {'alert':alert})
    print('e')
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
@cache_control(no_cache=True, must_revalidate=True, no_store = True)
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
        book.save()
        return render(request, "member/profile.html", {'alert':"The book has been issued to you!"})
    else:
        return render(request, "member/profile.html", {'alert':"You cannot issue this book currently. You have reached your maximum book issue limit!!"})


@login_required(login_url = '/member/login')
def view_current_issues(request):
    issued_books = request.user.member.book_set.all()
    reserved_book = request.user.member.reserved_book
    reserve_time = request.user.member.reserve_datetime
    active_member = reserved_book.member_set.all().order_by('reserve_datetime').first()
    if (active_member.user.username == request.user.username):
        reservation_status = "Active"
    else:
        reservation_status ="Pending"
    return render(request, "member/view_issued_books.html", {'issued_books':issued_books, 'reserved_book': reserved_book, 'reserve_time': reserve_time, 'reservation_status': reservation_status})


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
        member.reserve_datetime = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        member.save()
        return render(request, "member/profile.html", {'alert':"You have been added to the waiting list for reserving this book. You will be notified if you have an active reservation on this book!"})
        

        member.reserve_datetime = datetime.datetime.now()
        member.save()
        return render(request, "member/profile.html", {'alert':"You have been added to the waiting list for reserving this book. You will be notified if you have an active reservation on this book!"})


@login_required(login_url = '/member/login')
@cache_control(no_cache=True, must_revalidate=True, no_store = True)
def return_book(request, book_id):
    book = Book.objects.get(id = book_id)
    book.return_requested = True
    book.save()

    return render(request, "member/profile.html", {'alert':"Your return request has been sent. Please wait for confirmation."})


def member_logout(request):
    logout(request)
    return redirect("/member/login")

