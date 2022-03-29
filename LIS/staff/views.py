from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, HttpResponse
from member.models import Member, Reminder, IssueThread
from book.models import Book
import datetime
from .models import *
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta

PENALTY_PER_DAY = 5
# Create your views here.
clerk_cnt = 0


def staff_home_page(request):
    return render(request, "staff/home.html")


def staff_registration(request):

    if request.method == "POST":
        global clerk_cnt

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        insti_id = request.POST.get('insti_id',"")
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        staff_type = request.POST['staff_type']
        user_name = ""

        if staff_type == "LIBRARIAN":
            user_name = "LIBR_0"

        elif staff_type == "LIBRARY CLERK":
            user_name = "LIBC_" + str(clerk_cnt)
            clerk_cnt += 1

        if password != confirm_password:
            passnotmatch = True
            return render(request, "staff/staff_registration.html", {'passnotmatch': passnotmatch})

        user = User.objects.create_user(
            username=user_name, email=email, password=password, first_name=first_name, last_name=last_name)
        staff = Staff.objects.create(user=user)
        user.save()
        staff.save()
        return redirect('/staff/staff_login')

    return render(request, "staff/staff_registration.html")


@login_required(login_url='/staff_login')
def add_book(request):
    user_name = request.user.username
    user_name = user_name.split("_")[0]
    if user_name == "LIBC":
        if request.method == "POST":
            title = request.POST.get('title', "")
            print(title)
            author = request.POST.get('author', "")
            isbn = request.POST.get('isbn', 0)
            rack_number = request.POST.get('rack_number', "")
            books = Book.objects.create(
                title=title, author=author, isbn=isbn, rack_number=rack_number)
            books.save()
            alert = "The book with the given details has been successfully added to the portal!"
            return render(request, "staff/add_book.html", {'alert': alert})
        return render(request, "staff/add_book.html")
    else:
        return redirect("/403")


def sort_reservations(book):
    book_reservations = []
    for member in book.member_set.all().order_by('reserve_datetime'):
        book_reservations.append(member)
    return book_reservations

    
@login_required(login_url='/staff_login')
def view_books(request, msg=""):
    user_name = request.user.username
    user_name = user_name.split("_")[0]
    if user_name == "LIBC" or user_name == "LIBR":
        books = Book.objects.all()
        books_reservations = []
        for book in books:
            books_reservations.append(sort_reservations(book))
        navbar_extends = ""
        if user_name == "LIBC":
            navbar_extends = "staff/clerk_navbar.html"
        else:
            navbar_extends = "staff/librarian_navbar.html"
        books_details = zip(books, books_reservations)
        return render(request, "staff/view_books.html", {'books_details':books_details, 'total_books': len(books), 'is_clerk' : (user_name == "LIBC"), 'navbar_extends':navbar_extends, 'msg':msg})
    else:
        return redirect("/403")


@login_required(login_url='/staff_login')
def view_issued_books(request, msg=""):
    user_name = request.user.username
    user_name = user_name.split("_")[0]
    if user_name == "LIBC" or user_name == "LIBR":
        books = Book.objects.all()
        books = books.exclude(issue_date=None)

        due_dates = []
        for book in books:
            due_dates.append(book.issue_date + relativedelta(months=book.issue_member.book_duration))

        book_details = zip(books, due_dates)
        navbar_extends = ""
        if user_name == "LIBC":
            navbar_extends = "staff/clerk_navbar.html"
        else:
            navbar_extends = "staff/librarian_navbar.html"
        return render(request, "staff/view_issued_books.html", {'books': book_details, 'total_books': len(books), 'is_clerk': (user_name == "LIBC"), 'navbar_extends': navbar_extends, 'msg': msg})
    else:
        return redirect("/403")


@login_required(login_url='/staff_login')
def view_members(request):
    user_name = request.user.username

    user_name = user_name.split("_")[0]
    if user_name == "LIBC" or user_name == "LIBR":
        members = Member.objects.all()
        navbar_extends = ""
        if user_name == "LIBC":
            navbar_extends = "staff/clerk_navbar.html"
        else:
            navbar_extends = "staff/librarian_navbar.html"
        return render(request, "staff/view_members.html", {'members': members, 'is_librarian': (user_name == "LIBR"), 'navbar_extends': navbar_extends})
    else:
        return redirect("/403")


def delete_member(request, myid):
    user_name = request.user.username
    user_name = user_name.split("_")[0]

    if user_name == "LIBR":
        members = Member.objects.get(id=myid)
        members.user.delete()
        members.delete()
        return redirect("/staff/view_members")
    else:
        return redirect("/403")


@login_required(login_url='/staff_login')
def delete_book(request, myid):

    user_name = request.user.username
    user_name = user_name.split("_")[0]
    if user_name == "LIBC":
        book = Book.objects.get(id=myid)
        if book.issue_date == None or book.issue_date == "":
            book.delete()
            return redirect("/staff/view_books")
        else:
            return  view_books(request, "Cannot delete a book that is issued!")
    else:
        return redirect("/403")


def staff_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, "staff/login.html", {'alert': "Invalid login credentials. Please try again."})

        user_name = user.username.split('_')[0]

        if user_name != "LIBC" and user_name != "LIBR":
            # alert = True
            return render(request, "staff/login.html", {'alert': "The given username does not correspond to any staff member. Please enter a valid username."})

        if user is not None:
            login(request, user)
            navbar_extends = ""
            if user_name == "LIBC":
                navbar_extends = "staff/clerk_navbar.html"
            else:
                navbar_extends = "staff/librarian_navbar.html"
            return render(request, "staff/profile.html", {'user_name': user_name, 'navbar_extends': navbar_extends})
        else:
            alert = True
            return render(request, "staff/login.html", {'alert': alert})
    return render(request, "staff/login.html")


@login_required(login_url='/staff_login')
def profile(request):
    user_name = request.user.username
    user_name = user_name.split("_")[0]
    if user_name == "LIBC":
        return render(request, "staff/clerk_profile.html")
    elif user_name == "LIBR":
        return render(request, "staff/librarian_profile.html")
    else:
        return redirect("/403")


def Logout(request):
    logout(request)
    return redirect("/staff/staff_login")


def approve_return_request(request, msg=""):
    books = Book.objects.filter(return_requested=True)
    return render(request, "staff/approve_return_request.html", {'books': books, 'navbar_extends': "staff/clerk_navbar.html", 'alert': msg})

# TODO: ADD PENALTY FUNCTIONALITY ONCE NOTIFICATIONS IS DONE


def return_book_approved(request, bookid):
    book = Book.objects.get(id=bookid)

    # for issue history
    member = book.issue_member
    issue_date = book.issue_date
    return_date = datetime.date.today().isoformat()
    penalty = penalty_reminder(bookid)

    issue_instance = IssueThread.objects.create(member = member, book = book, issue_date = issue_date, return_date = return_date, penalty = penalty)
    issue_instance.save()
    book.issue_date = None
    book.issue_member = None
    book.return_requested = False
    book.save()
    return approve_return_request(request, "Book return approved successfully!")


def overdue_reminder(request, bookid):
    book_obj = Book.objects.get(id=bookid)
    reminder = Reminder.objects.create(rem_id = 'Overdue', message = "Your book is due to be returned!", penalty=0, book=book_obj, member=book_obj.issue_member, rem_datetime=datetime.datetime.now())
    reminder.save()
    return view_issued_books(request, "Reminder sent successfully!")


def penalty_reminder(bookid):
    book = Book.objects.get(id=bookid)

    if book.issue_date + relativedelta(months=book.issue_member.book_duration) >= datetime.date.today():
        penalty = 0
    else:
        day_diff = (datetime.date.today() - book.issue_date - relativedelta(months=book.issue_member.book_duration)).days
        penalty = day_diff * PENALTY_PER_DAY

    reminder = Reminder(rem_id = 'Penalty', message = "Your book return request is approved!", penalty=penalty, book=book, member=book.issue_member, rem_datetime=datetime.datetime.now())
    reminder.save()

    return penalty


def issue_statistics(request):
    pass
