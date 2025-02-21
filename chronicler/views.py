from django.shortcuts import render
from django.http import HttpResponse
from render_block import render_block_to_string
from django.contrib.auth.decorators import login_required
from django.db import models
from django.template import loader
from sums.models import Budgets, Users, Transactions, Accounts
from django.template.defaultfilters import slugify
from datetime import datetime
import json

# Create your views here.


@login_required
def index(request):
    unclassified = Transactions.objects.filter(budget_id__isnull=True, account_owner=request.user.username).values()
    budget_options = Budgets.objects.filter(username=request.user.username).values()
    for item in unclassified:
        item['transaction_date'] = item['transaction_date'].strftime('%b %d, %Y')
        item['amount'] = float(item['amount'])
    for item in budget_options:
        if item['monthly_budget'] is not None:
            item['monthly_budget'] = float(item['monthly_budget'])
        if item['annual_budget'] is not None:
            item['annual_budget'] = float(item['annual_budget'])
    request.session["unclassified"] = json.dumps(list(unclassified))
    request.session["budget_options"] = json.dumps(list(budget_options))
    return render(request, "Chronicle/index.html", context={"unclassified":list(unclassified), "options":list(budget_options)})