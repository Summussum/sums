from django.shortcuts import render
from django.http import HttpResponse
from render_block import render_block_to_string
from django.contrib.auth.decorators import login_required
from django.db import models
from django.template import loader
from sums.models import Budgets, User
from sums.graphs import return_pie
from django.template.defaultfilters import slugify

# Create your views here.
@login_required
def index(request):
    response = render(request, "Allocate/index.html")
    response["HX-Push-Url"] = request.path
    return response

@login_required
def create_budget_category(request):
    new_category_display = request.POST.get("category_display")
    if new_category_display == "":
        html = render_block_to_string("Allocate/error_partials.html", "no_category_name", request=request)
        response = HttpResponse(html)
        response["HX-Retarget"] = "#error_message"
        return response
    new_category_name = slugify(new_category_display)
    amount = request.POST.get("amount")
    if amount == "" or is_float(amount) == False:
        html = render_block_to_string("Allocate/error_partials.html", "no_amount", request=request)
        response = HttpResponse(html)
        response["HX-Retarget"] = "#error_message"
        return response
    if Budgets.objects.filter(category_name=new_category_name, user=request.user).exists():
        response = render_block_to_string("Allocate/error_partials.html", "already_exists", request=request)
        response = HttpResponse(html)
        response["HX-Retarget"] = "#error_message"
        return response
    else:
        if request.POST.get("annual"):
            new_budget = Budgets(user=request.user, category_name=new_category_name, category_display=new_category_display,annual_budget=amount)
        else:
            new_budget = Budgets(user=request.user,category_name=new_category_name,category_display=new_category_display,monthly_budget=amount)
        new_budget.save()
        return display_active_budget(request)

@login_required
def display_active_budget(request):
    category_list = []
    for object in Budgets.objects.filter(user=request.user):
        category_list.append(object)
    category_list = sorted(category_list, key=lambda x: x.category_name)
    graph_div = return_pie(request.user)
    context = {"category_list": category_list, "graph_div": graph_div}
    template = loader.get_template("Allocate/budget_display.html")
    return HttpResponse(template.render(context, request))

@login_required
def allocate(request, category_name):
    if request.method == 'GET':
        budget = Budgets.objects.filter(category_name=category_name, user=request.user).first()
        if budget.monthly_budget:
            amount = budget.monthly_budget
        else:
            amount = budget.annual_budget
        html = render_block_to_string("Allocate/allocator.html", "inline_editor", context={"item": budget, "amount": amount}, request=request)
        return HttpResponse(html)

    elif request.method == 'POST':

        new_category_display = request.POST.get("category_display")
        if new_category_display == "":
            html = render_block_to_string("Allocate/error_partials.html", "no_category_name", request=request)
            response = HttpResponse(html)
            response["HX-Retarget"] = f"#name_in_use{category_name}"
            response["HX-Reswap"] = "innerHTML"
            return response
        new_category_name = slugify(new_category_display)
        amount = request.POST.get("amount")
        if amount == "" or is_float(amount) == False:
            html = render_block_to_string("Allocate/error_partials.html", "no_amount", request=request)
            response = HttpResponse(html)
            response["HX-Retarget"] = f"#name_in_use{category_name}"
            response["HX-Reswap"] = "innerHTML"
            return response
        if Budgets.objects.filter(category_name=new_category_name).exists() and new_category_name != category_name:
            html = render_block_to_string("Allocate/error_partials.html", "already_exists", request=request)
            response = HttpResponse(html)
            response["HX-Retarget"] = f"#name_in_use{category_name}"
            response["HX-Reswap"] = "innerHTML"
            return response
        else:
            if request.POST.get("annual"):
                 new_budget = Budgets(user=request.user,category_name=new_category_name,category_display=new_category_display,annual_budget=amount)
            else:
                new_budget = Budgets(user=request.user,category_name=new_category_name, category_display=new_category_display,monthly_budget=amount)
            
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

def error_clear(request):
    html = render_block_to_string("Allocate/error_partials.html", "error_clear", request=request)
    response = HttpResponse(html)
    response["HX-Retarget"] = "#error_message"
    return response

def is_float(element: any) -> bool:
    #If you expect None to be passed:
    if element is None: 
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False

