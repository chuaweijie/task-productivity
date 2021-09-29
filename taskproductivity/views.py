import json, hashlib, time

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import IntegrityError, transaction
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import Paginator

from taskproductivity.models import User, Recoveries

# Create your views here.
@ensure_csrf_cookie
def index(request):
    # How to check if the user is already logged in? 
    return render(request, "taskproductivity/index.html")

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("tasks"))
        else:
            return render(request, "taskproductivity/login.html", {
                "type": "danger",
                "message": "Invalid username and/or password."
            }, status=401)
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
                "type": "warning",
                "message": "Passwords must match."
            }, status=400)

        # Attempt to create new user
        try:
            with transaction.atomic():
                user = User.objects.create_user(username, email, password)
                user.save()
        except IntegrityError:
            return render(request, "taskproductivity/signup.html", {
                "type": "warning",
                "message": "Username and/or email is already registered."
            }, status=400)
        login(request, user)
        # Should redirect to task in the future
        return HttpResponseRedirect(reverse("tasks"))
    else:
        return render(request, "taskproductivity/signup.html")

# route for the frontend js to check if email exists or not. 
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
        
# route for the frontend js to check if username exists or not. 
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

def tasks(request):
    if request.method == "GET":
        return render(request, "taskproductivity/tasks.html")
    else:
        raise PermissionDenied

def task_data(request, user_id, page_no):
    response = {}
    return JsonResponse(response)

def man_task(request):
    response = {}
    return JsonResponse(response)


def report(request):
    return render(request, "taskproductivity/report.html")

@ensure_csrf_cookie
def recovery(request):
    if request.method == "POST":
        email = request.POST["email"]
        mode = request.POST["mode"]

        # Mode switcher
        if mode == "trigger":
            print("in trigger")
            user = User.objects.get(email=email)
            recovery_data = user.recovery
            if recovery_data == None:
                hash = hashlib.sha384(b""+email+time.time()).hexdigest()
                print(f"hash: {hash}")
    return render(request, "taskproductivity/recovery.html")

@ensure_csrf_cookie
def recovery_key(request, key=None):
    if key is None:
        return render(request, "taskproductivity/index.html", {
                "type": "danger",
                "message": "Invalid recovery key"
            }, status=401)