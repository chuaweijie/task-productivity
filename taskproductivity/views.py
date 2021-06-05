from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "taskproductivity/index.html")

def login(request):
    return render(request, "taskproductivity/index.html")

def signup(request):
    return render(request, "taskproductivity/index.html")