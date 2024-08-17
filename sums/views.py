from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def sums_index(request):
    return render(request, "Login.html")

def sums_login(request):
    #return render(request, "logged_in.html")
    username = request.POST.get("user_name")
    context = {"username": username}
    template = loader.get_template("logged_in.html")
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Congratulations, User! You have been logged in")