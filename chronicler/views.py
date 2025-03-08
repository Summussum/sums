from django.shortcuts import render
from django.http import HttpResponse
from render_block import render_block_to_string
from django.contrib.auth.decorators import login_required
from django.db import models
from django.template import loader
from sums.models import Budgets, Users, Transactions, Accounts
from django.template.defaultfilters import slugify
from django.forms.models import model_to_dict
from datetime import datetime
import json

# Create your views here.


@login_required
def index(request):
    unclassified = Transactions.objects.filter(budget_id__isnull=True, account_owner=request.user.username).values()
    budget_options = Budgets.objects.filter(username=request.user.username).values()
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
    options = request.session["budget_options"]
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
    budget = Budgets.objects.filter(username=request.user.username, category_name=category_name).first()
    entry = Transactions.objects.filter(transaction_id=target['transaction_id']).first()
    entry.budget_id = budget.budget_id
    entry.save()
    entry.amount = float(entry.amount)
    entry.transaction_date = entry.transaction_date.strftime('%b %d, %Y')
    entry = model_to_dict(entry)
    request.session["chronicle_recent"].append(entry)
    request.session["budget_dict"] = get_budget_dict(request)
    chronicle_history = request.session["chronicle_recent"][-1:-11:-1]
    for item in chronicle_history:
        item["category_name"] = request.session["budget_dict"][item["budget_id"]]
    request, chronicle_target, options = new_target(request)
    if chronicle_target:
        html = render_block_to_string("Chronicle/partials.html", "chronicle", context={"target": chronicle_target, "chronicle_history": chronicle_history, "options": options}, request=request)
    else:
        html = render_block_to_string("Chronicle/partials.html", "complete", context={"chronicle_history": chronicle_history, "options": options}, request=request)
    return HttpResponse(html)


def categorize_new_budget(request):
    pass


def edit(request, transaction_id):
    category_name = request.POST.get("category_name")
    transaction_id = transaction_id
    options = request.session["budget_options"]
    entry = Transactions.objects.get(account_owner=request.user.username, transaction_id=transaction_id)
    if category_name == "None":
        entry.budget_id = None
        budget = None
    else:
        budget = Budgets.objects.get(username = request.user.username, category_name=category_name)
        entry.budget_id = budget.budget_id
    entry.category_name = category_name
    entry.save()
    test = []
    test.append(request.session["unclassified"])
    chronicle_recent = request.session.get("chronicle_recent")
    for i, item in enumerate(chronicle_recent):
        if item["transaction_id"] == transaction_id:
            item["category_name"] = category_name
            if budget is not None:
                item["budget_id"] = budget.budget_id
            else:
                item["budget_id"] = "None"
                item["category_name"] = "None"
                chronicle_load = request.session["unclassified"]
                chronicle_load.append(item)
                request.session["unclassified"] = chronicle_load
                chronicle_recent.pop(i)
                test.append(chronicle_recent)
                test.append(request.session["unclassified"])
            request.session["chronicle_recent"] = chronicle_recent
            break
    html = render_block_to_string("Chronicle/partials.html", "chronicle_line", context={"entry": entry, "options": options}, request=request)
    return HttpResponse(html)




def get_budget_dict(request):
    budgets = Budgets.objects.filter(username=request.user.username)
    budget_dict = {}
    for budget in budgets:
        budget_dict[budget.budget_id] = budget.category_name
    return budget_dict