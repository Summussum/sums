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

# Create your views here.
@login_required
def index(request):
    try:
        accounts = Accounts.objects.get(account_owner=request.user.username)
    except:
        accounts = []
    return render(request, "Import/index.html", context={"accounts": accounts})

@login_required
def csv_file_upload(request):

    files = []
    for file in request.FILES.values():
        filename = file.name
        if ".csv" in filename:
            files.append(file.read().decode("utf-8"))
            filename = file.name
            request.session["csv_files"] = files
        else:
            html = render_block_to_string("Import/partials.html", "failed", request=request)
            return HttpResponse(html)
    request.session["csv_files"] = files
    if request.POST.get("account") == "new":
        first_line = files[0].split("\n")[0].split(",")
        first_slugs = [slugify(header) for header in first_line]
        length = len(first_line)
        html = render_block_to_string("Import/accounts.html", "add_account", request=request, context={"first_line": first_line, "slugs": first_slugs, "length": length})
        return HttpResponse(html) 
    else:
        return csv_file_save(request)
    
    
    
    
@login_required
def csv_file_save(request):
    account_id = request.POST.get("account")
    translator = Accounts.objects.get(account_id=account_id).first()
    files = request.session["csv_files"]
    if files:
        for f in files:
            file = csv_transform.Transformer(f, translator)
            for line in file.record:
                entry = Transactions(amount=line["amount"], transaction_date=datetime.strptime(line["transaction_date"], '%d-%b-%Y').isoformat()[:10], transaction_description=line["transaction_description"])
                entry.save()

    context = {"filename": filename}
    html = render_block_to_string("Import/partials.html", "success", context=context, request=request)
    return HttpResponse(html)
    