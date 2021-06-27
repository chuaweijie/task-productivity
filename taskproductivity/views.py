import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import IntegrityError, transaction
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from taskproductivity.models import User

# Create your views here.
@ensure_csrf_cookie
def index(request):
    # How to check if the user is already logged in? 
    return render(request, "taskproductivity/index.html")

def login_view(request, user):
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
            return render(request, "taskproductivity/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "taskproductivity/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@ensure_csrf_cookie
def signup(request):
    if request.method == "POST":
        
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if password != confirmation:
            return render(request, "taskproductivity/signup.html", {
                "message": "Passwords must match."
            }, status=400)

        # Attempt to create new user
        try:
            with transaction.atomic():
                user = User.objects.create_user(username, email, password)
                user.save()
        except IntegrityError:
            return render(request, "taskproductivity/signup.html", {
                "message": "Username and/or email is already registered."
            }, status=400)
        login(request, user)
        # Should redirect to task in the future
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "taskproductivity/signup.html")

def email(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response = {
            "unique": False
        }

        try:
            User.objects.get(email=data.get("email"))
        except ObjectDoesNotExist: 
            response["unique"] = True
            
        return JsonResponse(response)
    else:
        raise PermissionDenied
        

def username(request):
    if request.method == "POST":            
        data = json.loads(request.body)
        response = {
            "unique": False
        }

        try:
            User.objects.get(username=data.get("username"))
        except ObjectDoesNotExist: 
            response["unique"] = True

        return JsonResponse(response)
    else:
        raise PermissionDenied