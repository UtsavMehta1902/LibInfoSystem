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
        staff_type = request.POST['staff_type']
        username = ""

        if staff_type == "LIBRARIAN":
            username= "LIBR_0"

        elif staff_type == "LIBRARY CLERK":
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
    user_name = request.user.username
    user_name = user_name.split("_")[0]
    if user_name == "LIBC":
        if request.method == "POST":
            title = request.POST.get('title',"")
            print(title)
            author = request.POST.get('author',"")
            isbn = request.POST.get('isbn',0)
            rack_number = request.POST.get('rack_number',"")
            books = Book.objects.create(title=title, author=author, isbn=isbn, rack_number=rack_number)
            books.save()
            alert = True
            return render(request, "staff/add_book.html", {'alert':alert})
        return render(request, "staff/add_book.html")  

    else:
        return redirect("/403")

@login_required(login_url = '/staff_login')
def view_books(request):
    user_name = request.user.username
    user_name = user_name.split("_")[0]
    if user_name == "LIBC" or user_name == "LIBR":
        books = Book.objects.all()
        return render(request, "staff/view_books.html", {'books':books})
    else:
        return redirect("/403")


@login_required(login_url = '/staff_login')
def view_members(request):
    user_name = request.user.username
    user_name = user_name.split("_")[0]
    if user_name == "LIBC" or user_name == "LIBR":
        members = Member.objects.all()
        return render(request, "staff/view_members.html", {'members':members})
    else:
        return redirect("/403")

def delete_member(request, myid):

    user_name = request.user.username
    user_name = user_name.split("_")[0]

    if user_name == "LIBR":   
        members = Member.objects.filter(id=myid)
        members.delete()
        return redirect("/staff/view_members")
    else:
        return redirect("/403")
    

@login_required(login_url = '/staff_login')
def delete_book(request, myid):

    user_name = request.user.username
    user_name = user_name.split("_")[0]
    if user_name == "LIBC":
        books = Book.objects.filter(id=myid)
        books.delete()
        return redirect("/staff/view_books")
    else:
        return redirect("/403")

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
    user_name = request.user.username
    user_name = user_name.split("_")[0]
    if user_name == "LIBC":
        return render(request, "staff/profile.html")
    else:
        return redirect("/403")


def Logout(request):
    logout(request)
    return redirect ("/staff/staff_login")

