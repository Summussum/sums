from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import models

# Create your views here.
#Pages:
def sums_index(request):
    return render(request, "dashboard.html")


# Partials:

def sums_login(request):

    #return render(request, "logged_in.html")
    username = request.POST.get("user_name")
    password = request.POST.get("password")
    context = {"username": username}
    template = loader.get_template("logged_in.html")
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Congratulations, User! You have been logged in")

def sums_register(request):
    return render(request, "register.html")

def new_user(request):
    pass