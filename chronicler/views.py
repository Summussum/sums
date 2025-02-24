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
    if request.session.get("chronicle_recent"):
        chronicle_history = request.session.get("chronicle_recent")[-1:-11:-1]
    else:
        request.session["chronicle_recent"] = []
        chronicle_history = []
    if unclassified:
        budget_options = Budgets.objects.filter(username=request.user.username).values()
        chronicle_load = []
        options = []
        for item in unclassified:
            item['transaction_date'] = item['transaction_date'].strftime('%b %d, %Y')
            item['amount'] = float(item['amount'])
            chronicle_load.append(item)
        for item in budget_options:
            if item['monthly_budget'] is not None:
                item['monthly_budget'] = float(item['monthly_budget'])
            if item['annual_budget'] is not None:
                item['annual_budget'] = float(item['annual_budget'])
            options.append(item)
        request.session["unclassified"] = chronicle_load
        request.session["budget_options"] = options
        request, chronicle_target, options = new_target(request)
        response = render(request, "Chronicle/index.html", context={"target":chronicle_target, "options":options, "chronicle_history": chronicle_history})
    else:
        response = render(request, "Chronicle/resolved.html", context={"chronicle_history": chronicle_history})
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
    chronicle_history = request.session["chronicle_recent"][-1:-11:-1]
    request, chronicle_target, options = new_target(request)
    if chronicle_target:
        html = render_block_to_string("Chronicle/partials.html", "chronicle", context={"target": chronicle_target, "chronicle_history": chronicle_history, "options": options}, request=request)
    else:
        html = render_block_to_string("Chronicle/partials.html", "complete", context={"chronicle_history": chronicle_history}, request=request)
    return HttpResponse(html)


def categorize_new_budget(request):
    pass