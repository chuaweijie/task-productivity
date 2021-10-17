from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("username", views.username, name="username"),
    path("email", views.email, name="email"),
    path("tasks", views.tasks, name="tasks"),
    path("task_data/<int:page_no>", views.task_data, name="task_data"),
    path("report", views.report, name="report"),
    path("recovery", views.recovery, name="recovery"),
    path("reset_password", views.reset_password, name="reset_password"),
    path("reset_password/<str:key>", views.reset_password, name="reset_password"),
    path("tracking", views.tracking, name="tracking"),
    path("history", views.history, name="history"),
]