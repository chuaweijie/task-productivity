from django.shortcuts import render

# Create your views here.
def index(request):
    # How to check if the user is already logged in? 
    return render(request, "taskproductivity/index.html")

def login(request):
    
    return render(request, "taskproductivity/login.html")

def signup(request):
    return render(request, "taskproductivity/signup.html")