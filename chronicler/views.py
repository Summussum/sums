from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sums.models import Transactions

# Create your views here.


@login_required
def index():
    unclassified = Transactions.objects.filter()

    pass