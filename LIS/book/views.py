from django.shortcuts import render

# Create your views here.

# function that is called when the home page is rendered
def home_page(request):
    return render(request, 'home.html')

# function to invoke the error_403 webpage when the user tries to access an unauthorised webpage
def error_403(request):
    return render(request, '403.html')