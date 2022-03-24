from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
UG_cnt=0
PG_cnt=0
RS_cnt=0
FAC_cnt=0

def member_registration(request):
    if request.method == "POST":
        global UG_cnt, PG_cnt, RS_cnt, FAC_cnt

        member_type = request.POST['member_type']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        username = ""
        limit=0
        duration=0

        if member_type == "UG":
            username= "UG_" + str(UG_cnt)
            UG_cnt+=1
            limit=2
            duration=1
        elif member_type == "PG":
            username= "PG_" + str(PG_cnt)
            PG_cnt+=1
            limit=4
            duration=1
        elif member_type == "RS":
            username= "RS_" + str(RS_cnt)
            RS_cnt+=1
            limit=6
            duration=3
        elif member_type == "FAC":
            username= "FAC_" + str(FAC_cnt)
            FAC_cnt+=1
            limit=10
            duration=6

        if password != confirm_password:
            passnotmatch = True
            return render(request, "member_registration.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        student = Member.objects.create(user=user, book_limit=limit, book_duration=duration)
        return redirect('/member/login')
        user.save()
        student.save()
        alert = True
        return render(request, "member_registration.html", {'alert':alert})
    return render(request, "member_registration.html")

@login_required(login_url = '/member/login')
def profile(request):
    return render(request, "profile.html")

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
                return redirect("/profile")
        else:
            alert = True
            return render(request, "member_login.html", {'alert':alert})
    return render(request, "member_login.html")
