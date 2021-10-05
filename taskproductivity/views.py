import json, hashlib

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import IntegrityError, transaction
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import Paginator
from django.utils import timezone

from .utils import send_email

from datetime import timedelta

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

        user = User.objects.filter(email__exact=email)
        if user.count() > 0:
            recovery_data = user[0].recovery
            # Hash the user's email and the current time
            key = ""+email+timezone.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
            hash = hashlib.sha224(key.encode('utf-8')).hexdigest()
            
            # Custom emaild data according to email template of mailjet.
            email_data = {
                "sender": "noreply@weijie.info",
                "sender_name": "90 Days Reporting Tracker",
                "to": email,
                "to_name": user[0].first_name + " " + user[0].last_name,
                "subject": "90 Days Reporting Tracker - Forgot your password?",
                "password_reset_button": "<a href='https://task-productivity.herokuapp.com/reset_password/" + hash + "'>Create a new password</a>",
                "password_reset_link": "<a href='https://task-productivity.herokuapp.com/reset_password/" + hash + "'>https://task-productivity.herokuapp.com/reset_password/" + hash + "</a>"
            }

            # Template ID from mailjet. 
            template_id = 3221171

            if recovery_data.count() > 0:
                old_keys = Recoveries.objects.filter(user=user[0], active=True).order_by('-time')
                # Only create new entry if past request is more than 5 minutes old to prevent spanning.
                timediff = timezone.now() - old_keys[0].time
                if timediff > timedelta(minutes=5):
                    old_keys.update(active=False)
                else:
                    return render(request, "taskproductivity/recovery.html", {
                        "type": "warning",
                        "message": "Please try to rest your password again after 5 minutes"
                    }, status=400)
               
            Recoveries.objects.create(user=user[0], key=hash)
            result = send_email(email_data, template_id)
            print(result.status_code)
            print(result.json())

        # The system will show this message regardless if the email exists or not so that hackers will not know if the email is in our system or not. 
        return render(request, "taskproductivity/recovery.html", {
                    "type": "success",
                    "message": "We've sent an email to " + email +" with instructions to reset your password. If you do not receive a password reset message after 1 minute, verify that you entered the correct email address, or check your spam folder."
                }, status=200)
                
    return render(request, "taskproductivity/recovery.html")

@ensure_csrf_cookie
def reset_password(request, key=None):    
    if request.method == "GET":
        if key is not None:
            keys = Recoveries.objects.filter(key=key, active=True).order_by('-time')
            if keys.count() > 0:
                return render(request, "taskproductivity/reset.html", {
                    "key": key
                })

        # When no key or an incorrect key is provided.
        return render(request, "taskproductivity/index.html", {
                "type": "danger",
                "message": "Invalid recovery key"
            }, status=401)

    elif request.method == "POST":
        recovery_key = request.POST["key"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        old_keys = Recoveries.objects.filter(key=recovery_key, active=True).order_by('-time')

        # If there is a key and the creation time and the current time is not more than 1 hour
        if old_keys.count() > 0:
            timediff = timezone.now() - old_keys[0].time
            if  timediff <= timedelta(hours=1):
                if password == confirmation:
                    user = User.get(old_keys[0].user)
                    user.set_password(password)
                    user.save()
                    old_keys.update(active=False)
                    return render(request, "taskproductivity/login.html", {
                        "type": "success",
                        "message": "You've successfully changed your password. Please login now."
                    }, status=200)
                
                # If passwords doesn't match
                return render(request, "taskproductivity/reset.html", {
                    "key": key,
                    "type": "warning",
                    "message": "Passwords don't match. Please make sure they are the same and try again."
                }, status=401)

        # Invalid key or expired key
        return render(request, "taskproductivity/recovery.html", {
            "type": "Error",
            "message": "Key error. Recovery key is probably older than 1 hour. Please request for the password reset and try again"
        }, status=400)