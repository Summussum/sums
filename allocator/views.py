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
    new_category_name = slugify(new_category_display)
    amount = request.POST.get("amount")
    if request.POST.get("annual"):
        annual_budget=True
    else:
        annual_budget=False
    if new_category_display == "":
        html = render_block_to_string("Allocate/error_partials.html", "no_category_name", request=request)
        response = HttpResponse(html)
        response["HX-Retarget"] = "#error_message"
        return response
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
    new_budget = Budgets(user=request.user, category_name=new_category_name, category_display=new_category_display, budget_amount=request.POST.get("amount"), annual_budget=annual_budget)
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
        if budget.budget_amount:
            amount = budget.budget_amount
        else:
            amount = budget.annual_budget
        html = render_block_to_string("Allocate/allocator.html", "inline_editor", context={"item": budget, "amount": amount}, request=request)
        return HttpResponse(html)

    elif request.method == 'POST':
        new_category_display = request.POST.get("category_display")
        new_category_name = slugify(new_category_display)
        amount = request.POST.get("amount")
        # error checks
        if new_category_display == "":
            html = render_block_to_string("Allocate/error_partials.html", "no_category_name", request=request)
            response = HttpResponse(html)
            response["HX-Retarget"] = f"#name_in_use{category_name}"
            response["HX-Reswap"] = "innerHTML"
            return response
        if amount == "" or is_float(amount) == False:
            html = render_block_to_string("Allocate/error_partials.html", "no_amount", request=request)
            response = HttpResponse(html)
            response["HX-Retarget"] = f"#name_in_use{category_name}"
            response["HX-Reswap"] = "innerHTML"
            return response
        if Budgets.objects.filter(category_name=new_category_name, user=request.user).exists() and new_category_name != category_name:
            html = render_block_to_string("Allocate/error_partials.html", "already_exists", request=request)
            response = HttpResponse(html)
            response["HX-Retarget"] = f"#name_in_use{category_name}"
            response["HX-Reswap"] = "innerHTML"
            return response
        # edit budget
        instance = Budgets.objects.filter(category_name=category_name).first()
        if request.POST.get("annual"):
            instance.annual_budget = True
        else:
            instance.annual_budget = False
        instance.category_display = new_category_display
        instance.category_name = new_category_name
        instance.budget_amount = amount
        instance.save()
        context = {"item": instance}
        html = render_block_to_string("Allocate/allocator.html", "data", context=context, request=request)
        return HttpResponse(html)


    elif request.method == 'DELETE':
        budget = Budgets.objects.filter(category_name=category_name).first()
        category_display = budget.category_display
        amount = budget.budget_amount
        budget.delete()
        html = f"<tr class='deletion'><td colspan='5'>Category named {category_display}: ${amount} has successfully been deleted.</td></tr>"
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

