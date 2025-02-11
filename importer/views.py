from django.shortcuts import render
from django.http import HttpResponse
from render_block import render_block_to_string
from django.contrib.auth.decorators import login_required
from django.db import models
from django.template import loader
from sums.models import Budgets, Users, Transactions, Accounts
from django.template.defaultfilters import slugify
from . import csv_transform
from datetime import datetime
import json

# Create your views here.
@login_required
def index(request):
    try:
        accounts = Accounts.objects.filter(account_owner=request.user.username)
    except:
        accounts = []
    response = render(request, "Import/index.html", context={"accounts": accounts})
    response["HX-Push-Url"] = request.path
    return response


@login_required
def csv_file_upload(request):

    files = []
    for file in request.FILES.values():
        filename = file.name
        if ".csv" in filename:
            files.append(file.read().decode("utf-8"))
            request.session["filename"] = file.name
        else:
            html = render_block_to_string("Import/partials.html", "failed", request=request)
            return HttpResponse(html)
    request.session["csv_files"] = files
    if request.POST.get("nickname") == "new":
        first_line = files[0].split("\n")[0].split(",")
        sample_lines = [line.split(",") for line in files[0].split("\n")[1:32:6]]
        first_slugs = [slugify(header) for header in first_line]
        html = render_block_to_string("Import/accounts.html", "add_account", request=request, context={"first_line": first_line, "slugs": first_slugs, "sample_lines": sample_lines})
        return HttpResponse(html) 
    else:
        return csv_file_save(request)
    

@login_required
def make_new_account(request):
    new_translator = {
        "transaction_date": request.POST.get("transaction_date"),
        "amount": request.POST.get("amount"),
        "transaction_description": request.POST.get("transaction_description"),
        "deposits": request.POST.get("deposits"),
        "notes": request.POST.get("additional")
        }
    if request.POST.get("neg_bool") == "on":
        negative_expenses_bool = True
    else:
        negative_expenses_bool = False
    new_account = Accounts(
        nickname = request.POST.get("nickname"),
        bank = request.POST.get("bank"),
        account_owner = Users.objects.get(username = request.user.username),
        account_type = request.POST.get("account_type"),
        account_last_four = request.POST.get("account_last_four"),
        translator = json.dumps(new_translator),
        date_formatter = request.POST.get("date_format"),
        negative_expenses = negative_expenses_bool
    )
    new_account.save()
    return csv_file_save(request)



    
    
@login_required
def csv_file_save(request):
    user = Users.objects.get(username=request.user.username)

    account_nickname = request.POST.get("nickname")
    account = Accounts.objects.get(account_owner=request.user.username, nickname=account_nickname)
    translator = account.translator
    date_format = account.date_formatter
    files = request.session["csv_files"]
    if files:
        for f in files:
            file = csv_transform.Transformer(f, translator, date_format)
            for line in file.record:
                entry = Transactions(amount=line["amount"], transaction_date=line["transaction_date"], transaction_description=line["transaction_description"], account_nickname=account.nickname, account_owner=user)
                entry.save()
    if request.path == "/importer/new_account/":
        accounts = [account]
    else:
        accounts = []
    context = {"filename": request.session["filename"], "accounts": accounts}
    html = render_block_to_string("Import/partials.html", "success", context=context, request=request)
    return HttpResponse(html)
    