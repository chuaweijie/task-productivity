from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

# Create your views here.
def index(request):
    # How to check if the user is already logged in? 
    return render(request, "taskproductivity/index.html")

def login(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "taskproductivity/login.html")

def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def signup(request):
    return render(request, "taskproductivity/signup.html")


