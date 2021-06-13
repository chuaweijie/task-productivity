from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.login, name="login"),
    path("", views.signup, name="signup"),
]