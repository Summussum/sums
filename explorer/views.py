from django.shortcuts import render
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def index(request):
    response = render(request, "Explore/index.html")
    response["HX-Push-Url"] = request.path
    return response

@login_required
def query_records(request):
    # category_name, category_display, date, budget_select(html selector with its own view), amount, description, recurring(checkbox), note(text edit, limit char display? except hover?)
    pass