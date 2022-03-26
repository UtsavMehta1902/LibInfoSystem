from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, HttpResponse
from member.models import Member
from book.models import Book
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
clerk_cnt=0

def staff_home_page(request):
    return render(request, "staff/home.html")

def staff_registration(request):

    if request.method == "POST":
        global clerk_cnt

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        username = ""
        
        username= "LIBC_" + str(clerk_cnt)
        clerk_cnt+=1

        if password != confirm_password:
            passnotmatch = True
            return render(request, "staff/staff_registration.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        staff = Staff.objects.create(user=user)
        # return redirect('/member/student_login')
        user.save()
        staff.save()
        alert = True
        return render(request, "staff/staff_registration.html", {'alert':alert})
    return render(request, "staff/staff_registration.html")


@login_required(login_url = '/staff_login')
def add_book(request):

    if request.method == "POST":
        title = request.POST.get('title',"")
        print(title)
        author = request.POST.get('author',"")
        isbn = request.POST.get('isbn',0)

        books = Book.objects.create(title=title, author=author, isbn=isbn)
        books.save()
        alert = True
        return render(request, "staff/add_book.html", {'alert':alert})
    return render(request, "staff/add_book.html")


@login_required(login_url = '/staff_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "staff/view_books.html", {'books':books})


@login_required(login_url = '/staff_login')
def view_members(request):
    members = Member.objects.all()
    return render(request, "staff/view_members.html", {'members':members})


@login_required(login_url = '/staff_login')
def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("/staff/view_books")


@login_required(login_url = '/staff_login')
def delete_member(request, myid):
    members = Member.objects.filter(id=myid)
    members.delete()
    return redirect("/staff/view_members")


def staff_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/staff/profile")
            
        else:
            alert = True
            return render(request, "staff/login.html", {'alert':alert})
    return render(request, "staff/login.html")


@login_required(login_url = '/staff_login')
def profile(request):
    return render(request, "staff/profile.html")


def Logout(request):
    logout(request)
    return redirect ("/staff/staff_login")


    
