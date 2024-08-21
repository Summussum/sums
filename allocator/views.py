from django.shortcuts import render
from django.http import HttpResponse
from render_block import render_block_to_string
from django.db import models
from django.template import loader
from sums.models import Budgets, Users
from sums.graphs import return_pie, return_pie3

# Create your views here.

def index(request):
    return render(request, "Allocate/index.html")

def create_budget_category(request):
    user = Users.objects.get(username="test")
    new_category_name = request.POST.get("category_name")
    amount = request.POST.get("amount")
    if Budgets.objects.filter(category_name=new_category_name).exists():
        response = render(request, "Allocate/category_already_exists.html")
        response["HX-Retarget"] = "#category_already_exists"
        return response
    else:
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
    graph_div = return_pie3()
    context = {"category_list": category_list, "graph_div": graph_div}
    template = loader.get_template("Allocate/budget_display.html")
    return HttpResponse(template.render(context, request))

def allocate(request, category_name):
    if request.method == 'GET':
        context = {"category_name": category_name}
        html = render_block_to_string("Allocate/allocator.html", "editor", context=context, request=request)
        # html = ""
        return HttpResponse(html)

    elif request.method == 'POST':

        user = Users.objects.get(username="test")
        new_category_name = request.POST.get("category_name")
        amount = request.POST.get("amount")

        if Budgets.objects.filter(category_name=new_category_name).exists() and new_category_name != category_name:
            response = render(request, "Allocate/category_already_exists.html")
            response["HX-Retarget"] = "#name_in_use"
            return response
        else:
            if request.POST.get("annual"):
                 new_budget = Budgets(username=user,category_name=new_category_name,annual_budget=amount)
            else:
                new_budget = Budgets(username=user,category_name=new_category_name,monthly_budget=amount)
            
            instance = Budgets.objects.filter(category_name=category_name)
            instance.delete()
            new_budget.save()
            return display_active_budget(request)


    elif request.method == 'DELETE':
        instance = Budgets.objects.filter(category_name=category_name)
        budget = instance.first()
        if budget.monthly_budget:
            amount = budget.monthly_budget
        elif budget.annual_budget:
            amount = budget.annual_budget
        else:
            amount = 0
        instance.delete()
        html = f"<tr><td>Category named {category_name}: ${amount} has successfully been deleted.</td></tr>"
        return HttpResponse(html)

def reset(request, category_name):
    return display_active_budget(request)
    """budget = Budgets.objects.filter(category_name=category_name).first()
    context = {"category_name": budget.category_name, "monthly_budget": budget.monthly_budget, "annual_budget": budget.annual_budget}
    html = render_block_to_string("Allocate/allocator.html", "data", context=context, request=request)
    return HttpResponse(html)"""

