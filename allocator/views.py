from django.shortcuts import render
from django.http import HttpResponse
from django_htmx.http import retarget
from django.db import models
from django.template import loader
from sums.models import Budgets, Users

# Create your views here.

def index(request):
    return render(request, "Allocate/index.html")

def create_budget_category(request):
    user = Users.objects.get(username="test")
    new_category_name = request.POST.get("category_name")
    amount = request.POST.get("amount")
    try:
        Budgets.objects.filter(new_category_name)
        response = render(request, "Allocate/category_already_exists.html")
        return retarget(response, "#category_already_exists")
    except:
        if request.POST.get("annual"):
            new_budget = Budgets(username=user,category_name=new_category_name,annual_budget=amount)
        else:
            new_budget = Budgets(username=user,category_name=new_category_name,monthly_budget=amount)
        new_budget.save()
        return display_active_budget(request)

def display_active_budget(request):
    category_list = []
    for object in Budgets.objects.all():
        category_list.append(object)
    context = {"category_list": category_list}
    template = loader.get_template("Allocate/budget_display.html")
    return HttpResponse(template.render(context))


