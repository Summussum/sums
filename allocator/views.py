from django.shortcuts import render
from django.http import HttpResponse
from render_block import render_block_to_string
from django.contrib.auth.decorators import login_required
from django.db import models
from django.template import loader
from sums.models import Budgets, Users
from sums.graphs import return_pie
from django.template.defaultfilters import slugify

# Create your views here.
@login_required
def index(request):
    return render(request, "Allocate/index.html")

@login_required
def create_budget_category(request):
    user = Users.objects.get(username=request.user.username)
    new_category_display = request.POST.get("category_display")
    new_category_name = slugify(new_category_display)
    amount = request.POST.get("amount")
    if Budgets.objects.filter(category_name=new_category_name).exists():
        response = render(request, "Allocate/category_already_exists.html")
        response["HX-Retarget"] = "#error_message"
        return response
    else:
        if request.POST.get("annual"):
            new_budget = Budgets(username=user,category_name=new_category_name, category_display=new_category_display,annual_budget=amount)
        else:
            new_budget = Budgets(username=user,category_name=new_category_name,category_display=new_category_display,monthly_budget=amount)
        new_budget.save()
        return display_active_budget(request)

@login_required
def display_active_budget(request):
    category_list = []
    for object in Budgets.objects.filter(username=request.user.username):
        category_list.append(object)
    category_list = sorted(category_list, key=lambda x: x.category_name)
    graph_div = return_pie()
    context = {"category_list": category_list, "graph_div": graph_div}
    template = loader.get_template("Allocate/budget_display.html")
    return HttpResponse(template.render(context, request))

@login_required
def allocate(request, category_name):
    if request.method == 'GET':
        budget = Budgets.objects.filter(category_name=category_name, username=request.user.username).first()
        if budget.monthly_budget:
            amount = budget.monthly_budget
        else:
            amount = budget.annual_budget
        html = render_block_to_string("Allocate/allocator.html", "inline_editor", context={"item": budget, "amount": amount}, request=request)
        return HttpResponse(html)

    elif request.method == 'POST':

        user = Users.objects.get(username=request.user.username)
        new_category_display = request.POST.get("category_display")
        new_category_name = slugify(new_category_display)
        amount = request.POST.get("amount")

        if Budgets.objects.filter(category_name=new_category_name).exists() and new_category_name != category_name:
            response = render(request, "Allocate/category_already_exists.html")
            response["HX-Retarget"] = "#name_in_use"
            return response
        else:
            if request.POST.get("annual"):
                 new_budget = Budgets(username=user,category_name=new_category_name,category_display=new_category_display,annual_budget=amount)
            else:
                new_budget = Budgets(username=user,category_name=new_category_name, category_display=new_category_display,monthly_budget=amount)
            
            instance = Budgets.objects.filter(category_name=category_name)
            instance.delete()
            new_budget.save()
            budget = Budgets.objects.filter(category_name=new_budget.category_name).first()
            context = {"item": budget}
            html = render_block_to_string("Allocate/allocator.html", "data", context=context, request=request)
            return HttpResponse(html)


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
        html = f"<tr class='deletion'><td></td><td></td><td>Category named {category_name}: ${amount} has successfully been deleted.</td><td></td><td></td></tr>"
        return HttpResponse(html)

@login_required
def reset(request, category_name):
    budget = Budgets.objects.filter(category_name=category_name).first()
    context = {"item": budget}
    html = render_block_to_string("Allocate/allocator.html", "data", context=context, request=request)
    return HttpResponse(html)

