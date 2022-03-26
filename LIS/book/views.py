from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request, 'home.html')

def error_403(request):
    return render(request, '403.html')