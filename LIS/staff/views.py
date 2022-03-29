from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, HttpResponse
from member.models import Member, Reminder, IssueThread
from book.models import Book
import datetime
from .models import *
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta

PENALTY_PER_DAY = 5
clerk_cnt = 0

# function to register a new staff member: Librarian and Clerks (a Librarian can be registered into the software only once, as a Library has only one Librarian) 
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

        if password != confirm_password:
            passnotmatch = True
            return render(request, "staff/staff_registration.html", {'passnotmatch': 'Passwords do not match!'})

        user = User.objects.create_user(
            username=user_name, email=email, password=password, first_name=first_name, last_name=last_name)
        staff = Staff.objects.create(user=user)
        user.save()
        staff.save()
        return redirect('/staff/staff_login')

    return render(request, "staff/staff_registration.html")


# this function requires a staff member to login and hence cannot be accessed by a normal member
@login_required(login_url='/staff_login')
def add_book(request):
    user_name = request.user.username
    user_name = user_name.split("_")[0]

    # only clerks are allowed to add a book, and not the Librarian
    if user_name == "LIBC":
        if request.method == "POST":
            title = request.POST.get('title', "")
            author = request.POST.get('author', "")
            isbn = request.POST.get('isbn', 0)
            rack_number = request.POST.get('rack_number', "")
            books = Book.objects.create(
                title=title, author=author, isbn=isbn, date_added=datetime.date.today(), rack_number=rack_number)
            books.save()
            alert = "The book with the given details has been successfully added to the portal!"
            return render(request, "staff/add_book.html", {'alert': alert})
        return render(request, "staff/add_book.html")
    
    else:    # if the user is a Librarian
        return redirect("/403")

# helper function to sort the current reservations of a book by the date and time of reservation in the order oldest request first
def sort_reservations(book):
    book_reservations = []
    try:
        for member in book.member_set.all().order_by('reserve_datetime'):
            book_reservations.append(member)
    except(Exception):
        pass
    return book_reservations

    
@login_required(login_url='/staff_login')

# function to allow the Librarian or clerk to view all the books in the Library as well as who all have reserved or issued that book
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

def activate_reservation(book):
    try:
        active_member = sort_reservations(book)[0]
    except(Exception):
        active_member = None
    if active_member is not None:
        reservation_reminder(active_member, book)
        
    return book


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
    book = activate_reservation(book)
    book.save()
    return approve_return_request(request, "Book return approved successfully!")


def overdue_reminder(request, bookid):
    book_obj = Book.objects.get(id=bookid)
    type = ""
    msg = ""

    if book_obj.issue_date + relativedelta(months=book_obj.issue_member.book_duration) < datetime.date.today():
        type = "Overdue"
        msg = "Book return date is overdue!"
    else:
        days = ((book_obj.issue_date + relativedelta(months=book_obj.issue_member.book_duration)) - datetime.date.today()).days
        type = "Due"
        msg = f"Book return date is {days} away!"

    reminder = Reminder.objects.create(rem_id = type, message = msg, penalty=0, book=book_obj, member=book_obj.issue_member, rem_datetime=datetime.datetime.now())
    reminder.save()
    return view_issued_books(request, "Reminder sent successfully!")


def penalty_reminder(bookid):
    book = Book.objects.get(id=bookid)

    if book.issue_date + relativedelta(months=book.issue_member.book_duration) >= datetime.date.today():
        penalty = 0
    else:
        day_diff = (datetime.date.today() - (book.issue_date + relativedelta(months=book.issue_member.book_duration))).days
        penalty = day_diff * PENALTY_PER_DAY

    reminder = Reminder(rem_id = 'Penalty', message = "Your book return request is approved!", penalty=penalty, book=book, member=book.issue_member, rem_datetime=datetime.datetime.now())
    reminder.save()

    return penalty


def reservation_reminder(active_member, book):
    reminder = Reminder.objects.create(rem_id = 'Reserved', message = "Your book reservation is now active.", penalty=0, book=book, member=active_member, rem_datetime=datetime.datetime.now())
    reminder.save()
    return


def issue_statistics(request):
    books = Book.objects.all()
    not_issued_5 = []
    not_issued_3 = []
    for book in books:
        if book.date_added is not None:
            if book.date_added + relativedelta(years=5) < datetime.date.today():
                if book.last_issued_date is None or book.last_issued_date  + relativedelta(years=5) < datetime.date.today():
                    not_issued_5.append(book)
            if book.date_added + relativedelta(years=3) < datetime.date.today():
                if book.last_issued_date is None or book.last_issued_date  + relativedelta(years=3) < datetime.date.today():
                    not_issued_3.append(book)

    return render(request, "staff/book_issue_statistics.html", {'not_issued_3': not_issued_3, 'not_issued_5': not_issued_5, 'navbar_extends': "staff/librarian_navbar.html",})
