from django.shortcuts import render
from django.http import HttpResponse
from render_block import render_block_to_string
from django.contrib.auth.decorators import login_required
from django.db import models
from django.template import loader
from sums.models import Budgets, Users, Transactions
from django.template.defaultfilters import slugify
from . import csv_transform
from datetime import datetime

# Create your views here.
@login_required
def index(request):
    return render(request, "Import/index.html")

@login_required
def csv_file_upload(request):
    translator = {
        "amount": "Withdrawals",
        "transaction_date": "Date",
        "transaction_description": "Description"
        }
    files = []
    for file in request.FILES.values():
        filename = file.name
        if ".csv" in filename:
            files.append(file.read().decode("utf-8"))
            filename = file.name
        else:
            html = render_block_to_string("Import/partials.html", "failed", request=request)
            return HttpResponse(html)
    if files:
        for f in files:
            file = csv_transform.Transformer(f, translator)
            for line in file.record:
                entry = Transactions(amount=line["amount"], transaction_date=datetime.strptime(line["transaction_date"], '%d-%b-%Y').isoformat()[:10], transaction_description=line["transaction_description"])
                entry.save()

    context = {"filename": filename}
    html = render_block_to_string("Import/partials.html", "success", context=context, request=request)
    return HttpResponse(html)
    