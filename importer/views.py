from django.shortcuts import render
from django.http import HttpResponse
from render_block import render_block_to_string
from django.db import models
from django.template import loader
from sums.models import Budgets, Users
from sums.graphs import return_pie
from django.template.defaultfilters import slugify

# Create your views here.
def importer_index(request):
    return render(request, "Import/index.html")