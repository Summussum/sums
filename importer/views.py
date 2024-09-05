from django.shortcuts import render
from django.http import HttpResponse
from render_block import render_block_to_string
from django.db import models
from django.template import loader
from sums.models import Budgets, Users, Transactions
from django.template.defaultfilters import slugify
from . import csv_transform
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, "Import/index.html")

def csv_file_upload(request):
    translator = {
        "amount": "Withdrawals",
        "transaction_date": "Date",
        "transaction_description": "Description"
        }
    files = []
    for file in request.FILES.values():
        files.append(file.read().decode("utf-8"))
    message = []
    # message.append(files)
    if files:
        for f in files:
            file = csv_transform.Transformer(f, translator)
            for line in file.record:
                entry = Transactions(amount=line["amount"], transaction_date=datetime.strptime(line["transaction_date"], '%d-%b-%Y').isoformat(), transaction_description=line["transaction_description"])
                message.append(line)
                entry.save()
                message.append(line)

    context = {"filename": message}
    html = render_block_to_string("Import/upload_result.html", "success", context=context, request=request)
    return HttpResponse(html)
    