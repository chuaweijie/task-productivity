from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("username", views.username, name="username"),
    path("email", views.email, name="email"),
    path("speech", views.speech, name="speech"),
]