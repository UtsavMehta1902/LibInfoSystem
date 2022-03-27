from operator import truediv
import re
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
# UG_cnt=0
# PG_cnt=0
# RS_cnt=0
# FAC_cnt=0

def member_home_page(request):
    return render(request, "member/home.html")

def member_registration(request):
    if request.method == "POST":
        # global UG_cnt, PG_cnt, RS_cnt, FAC_cnt

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
            # UG_cnt+=1
            limit=2
            duration=1
        elif member_type == "PG":
            username= "PG_" + str(insti_id)
            # PG_cnt+=1
            limit=4
            duration=1
        elif member_type == "RS":
            username= "RS_" + str(insti_id)
            # RS_cnt+=1
            limit=6
            duration=3
        elif member_type == "FAC":
            username= "FAC_" + str(insti_id)
            # FAC_cnt+=1
            limit=10
            duration=6

        if password != confirm_password:
            passnotmatch = True
            return render(request, "member/registration.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        member = Member.objects.create(insti_id=insti_id, user=user, book_limit=limit, book_duration=duration)
        return redirect('/member/login')
        user.save()
        member.save()
        alert = True
        return render(request, "member/registration.html", {'alert':alert})
    return render(request, "member/registration.html")

@login_required(login_url = '/member/login')
def profile(request):
    user_name = request.user.username
    user_name = user_name.split("_")[0]
    is_faculty = False
    if(user_name == "FAC"):
        is_faculty = True
    

    return render(request, "member/profile.html", {'is_faculty': is_faculty})

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

# @login_required(login_url = '/member/login')
def member_logout(request):
    logout(request)
    return redirect("/member/login")