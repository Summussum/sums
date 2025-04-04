from django.shortcuts import render
from django.http import HttpResponse
from render_block import render_block_to_string
from django.contrib.auth.decorators import login_required
from django.db import models
from django.template import loader
from sums.models import Budgets, User, Transactions, Accounts
from django.template.defaultfilters import slugify
from . import csv_transform
from datetime import datetime
import json

# Create your views here.
@login_required
def index(request):
    try:
        accounts = Accounts.objects.filter(user=request.user)
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
        auto_amount, auto_date, auto_description, auto_deposits = "", "", "", ""
        for header in first_line[-1::-1]:
            if any(keyword in header.lower() for keyword in ["withdraw", "expens", "amount", "debit"]):
                auto_amount = f"<option value='{header}'>{header}</option>"
            elif any(keyword in header.lower() for keyword in ["date"]):
                auto_date = f"<option value='{header}'>{header}</option>"
            elif any(keyword in header.lower() for keyword in ["descrip", "detail"]):
                auto_description = f"<option value='{header}'>{header}</option>"
            elif any(keyword in header.lower() for keyword in ["deposit", "credit"]):
                auto_deposits = f"<option value='{header}'>{header}</option>"
        context = {"first_line": first_line, "slugs": first_slugs, "sample_lines": sample_lines, "auto_amount": auto_amount, "auto_date": auto_date, "auto_description": auto_description, "auto_deposits": auto_deposits}
        html = render_block_to_string("Import/accounts.html", "add_account", request=request, context=context)
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
    pop_list = []
    for key in new_translator:
        if new_translator[key] == "None":
            pop_list.append(key)
    for item in pop_list:
        new_translator.pop(item)
    new_account = Accounts(
        nickname = request.POST.get("nickname"),
        bank = request.POST.get("bank"),
        user = request.user,
        account_type = request.POST.get("account_type"),
        account_last_four = request.POST.get("account_last_four"),
        translator = json.dumps(new_translator),
        date_formatter = request.POST.get("date_format"),
    )
    new_account.save()
    return csv_file_save(request)



    
    
@login_required
def csv_file_save(request):

    account_nickname = request.POST.get("nickname")
    account = Accounts.objects.get(user=request.user, nickname=account_nickname)
    translator = account.translator
    date_format = account.date_formatter
    files = request.session["csv_files"]
    if files:
        for f in files:
            file = csv_transform.Transformer(f, translator, date_format)
            for line in file.record:
                entry = Transactions(amount=line["amount"], transaction_date=line["transaction_date"], transaction_description=line["transaction_description"], account=account, user=request.user)
                entry.save()
    if request.path == "/importer/new_account/":
        accounts = [account]
    else:
        accounts = []
    context = {"filename": request.session["filename"], "accounts": accounts}
    html = render_block_to_string("Import/partials.html", "success", context=context, request=request)
    return HttpResponse(html)
    