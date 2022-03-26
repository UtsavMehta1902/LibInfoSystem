from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("add_book/", views.add_book, name="add_book"),
    path("view_books/", views.view_books, name="view_books"),
    path("view_members/", views.view_members, name="view_members"),
    #path("issue_book/", views.issue_book, name="issue_book"),
    #path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
    # path("student_issued_books/", views.student_issued_books, name="student_issued_books"),
    # path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("staff_registration/", views.staff_registration, name="staff_registration"),
    #path("change_password/", views.change_password, name="change_password"),
    # path("student_login/", views.student_login, name="student_login"),
    path("staff_login/", views.staff_login, name="staff_login"),
    path("logout/", views.Logout, name="logout"),
    path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
    path("delete_member/<int:myid>/", views.delete_member, name="delete_member"),
]