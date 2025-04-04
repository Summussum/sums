from django.shortcuts import render
from django.http import HttpResponse
from render_block import render_block_to_string
from django.contrib.auth.decorators import login_required
from django.db import models
from django.template import loader
from sums.models import Budgets, User, Transactions, Accounts
from allocator.views import create_budget_category
from django.template.defaultfilters import slugify
from django.forms.models import model_to_dict
from datetime import datetime
import json

# Create your views here.


@login_required
def index(request):
    unclassified = Transactions.objects.filter(budget__isnull=True, user=request.user).values('account__nickname', 'transaction_id', 'amount', 'transaction_date', 'transaction_description', 'budget', 'note', 'recurring', 'user', 'account')
    budget_options = Budgets.objects.filter(user=request.user).values()
    options = []
    for item in budget_options:
        if item['monthly_budget'] is not None:
            item['monthly_budget'] = float(item['monthly_budget'])
        if item['annual_budget'] is not None:
            item['annual_budget'] = float(item['annual_budget'])
        options.append(item)
    request.session["budget_options"] = options
    if request.session.get("chronicle_recent"):
        chronicle_history = request.session.get("chronicle_recent")[-1:-11:-1]
    else:
        request.session["chronicle_recent"] = []
        chronicle_history = []
    if unclassified:
        chronicle_load = []
        for item in unclassified:
            item['transaction_date'] = item['transaction_date'].strftime('%b %d, %Y')
            item['amount'] = float(item['amount'])
            chronicle_load.append(item)

        request.session["unclassified"] = chronicle_load
        request, chronicle_target, options = new_target(request)
        response = render(request, "Chronicle/index.html", context={"target":chronicle_target, "options":options, "chronicle_history": chronicle_history})
    else:
        response = render(request, "Chronicle/resolved.html", context={"chronicle_history": chronicle_history, "options": options})
    response["HX-Push-Url"] = request.path
    return response



def new_target(request):
    budget_options = Budgets.objects.filter(user=request.user).values()
    options = []
    for item in budget_options:
        if item['monthly_budget'] is not None:
            item['monthly_budget'] = float(item['monthly_budget'])
        if item['annual_budget'] is not None:
            item['annual_budget'] = float(item['annual_budget'])
        options.append(item)
    request.session["budget_options"] = options
    if request.session["unclassified"]:
        chronicle_target = request.session["unclassified"].pop()
        request.session["chronicle_target"] = chronicle_target
        return request, chronicle_target, options
    else:
        chronicle_target = []
        return request, chronicle_target, options

        


def assign(request):
    target = request.session["chronicle_target"]
    category_name = request.POST.get("category_name")
    budget = Budgets.objects.filter(user=request.user, category_name=category_name).first()
    entry = Transactions.objects.filter(transaction_id=target['transaction_id']).first()
    entry.budget = budget
    entry.save()
    entry_dict = Transactions.objects.filter(transaction_id=target['transaction_id']).values('account__nickname', 'transaction_id', 'amount', 'transaction_date', 'transaction_description', 'budget', 'note', 'recurring', 'user', 'account').first()
    entry_dict["amount"] = float(entry_dict["amount"])
    entry_dict["transaction_date"] = entry_dict["transaction_date"].strftime('%b %d, %Y')
    entry_dict["budget__category_display"] = budget.category_display
    entry_dict["budget__category_name"] = budget.category_name
    request.session["chronicle_recent"].append(entry_dict)
    chronicle_history = request.session["chronicle_recent"][-1:-11:-1]
    request, chronicle_target, options = new_target(request)
    if chronicle_target:
        html = render_block_to_string("Chronicle/partials.html", "chronicle", context={"target": chronicle_target, "chronicle_history": chronicle_history, "options": options}, request=request)
    else:
        html = render_block_to_string("Chronicle/partials.html", "complete", context={"chronicle_history": chronicle_history, "options": options}, request=request)
    return HttpResponse(html)


def new_budget(request):
    create_budget_category(request)
    mutable = request.POST._mutable
    request.POST._mutable = True
    request.POST["category_name"] = slugify(request.POST["category_display"])
    request.POST._mutable = mutable
    return assign(request)


def edit(request, transaction_id):
    category_name = request.POST.get("category_name")
    transaction_id = transaction_id
    options = request.session["budget_options"]
    entry = Transactions.objects.get(user=request.user, transaction_id=transaction_id)
    if category_name == "None":
        entry.budget = None
        budget = None
    else:
        budget = Budgets.objects.get(user = request.user, category_name=category_name)
        entry.budget = budget
    entry.save()
    entry.account__nickname = entry.account.nickname
    entry.budget__category_name = category_name
    if budget:
        entry.budget__category_display = budget.category_display
    else:
        entry.budget__category_display = "None"
    chronicle_recent = request.session.get("chronicle_recent")
    for i, item in enumerate(chronicle_recent):
        if item["transaction_id"] == transaction_id:
            item["category_name"] = entry.budget__category_name
            item["category_display"] = entry.budget__category_display
            if budget is not None:
                item["budget"] = budget.budget_id
            else:
                item["budget"] = "None"
                chronicle_load = request.session["unclassified"]
                chronicle_load.append(item)
                request.session["unclassified"] = chronicle_load
                chronicle_recent.pop(i)
            request.session["chronicle_recent"] = chronicle_recent
            break
    html = render_block_to_string("Chronicle/partials.html", "chronicle_line", context={"entry": entry, "options": options}, request=request)
    return HttpResponse(html)



"""
def get_budget_dict(request):
    budgets = Budgets.objects.filter(user=request.user)
    budget_dict = {}
    for budget in budgets:
        budget_dict[budget] = budget.category_name
    return budget_dict"
"""