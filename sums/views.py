from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import models
from render_block import render_block_to_string
from django_htmx.http import HttpResponseClientRedirect
from django.shortcuts import redirect


# Create your views here.
#Pages:
@login_required
def sums_index(request):
    if request.user.is_authenticated:
        context = {"username": request.user.username}
    else:
        context = {"username": "anonymous user"}
    response = render(request, "dashboard.html", context=context)
    response["HX-Push-Url"] = request.path
    return response

def sums_entrypoint(request):
    return render(request, "Login/index.html")

def sums_login_form(request):
    html = render_block_to_string("Login/login.html", "login", request=request)
    return HttpResponse(html)

def sums_login_submit(request):
    val_username = request.POST.get("user_name")
    val_password = request.POST.get("password")
    user = authenticate(request, username=val_username, password=val_password)
    if user is not None:
        login(request, user)
        response = render(request, "dashboard.html", context={"username": user.username})
        response["Hx-Redirect"] = "/"
        return response
    else:
        html = render_block_to_string("Login/welcome_text.html", "nonlogin", request=request)
        return HttpResponse(html)


def sums_register_form(request):
    html = render_block_to_string("Login/login.html", "register", request=request)
    return HttpResponse(html)
    
def sums_register_submit(request):
    new_username = request.POST.get("user_name")
    new_email = request.POST.get("email")
    new_password = request.POST.get("password")
    user = User.objects.create_user(new_username, new_email, new_password)
    user.save()
    new_user = User.objects.filter(username=new_username).first()
    if new_user:
        context = {"user": new_user}
        html = render_block_to_string("Login/welcome_text.html", "registered", context=context, request=request)
    else:
        html = render_block_to_string("Login/welcome_text.html", "nonregistered", request=request)
    return HttpResponse(html)

def sums_logout(request):
    logout(request)
    return redirect("/")
