from django.shortcuts import render
from django.http import HttpResponse
from render_block import render_block_to_string
from django.contrib.auth.decorators import login_required
from sums.models import Transactions, Budgets



# Create your views here.
@login_required
def index(request):
    budgets = Budgets.objects.filter(username=request.user.username)
    budget_dict = {}
    for budget in budgets:
        budget_dict[budget.budget_id] = (budget.category_name, budget.category_display)
    response = render(request, "Explore/index.html", context={"budget_select": str(budget_dict)})
    response["HX-Push-Url"] = request.path
    return response

@login_required
def query_records(request):
    # category_name, category_display, date, budget_select(html selector with its own view), amount, description, recurring(checkbox), note(text edit, limit char display? except hover?)
    budgets = Budgets.objects.filter(username=request.user.username)
    budget_dict = {}
    for budget in budgets:
        budget_dict[budget.budget_id] = budget.category_display
    budget_select = render_block_to_string("Explore/partials.html", "budget_select", context={"budgets": budgets})
    records = Transactions.objects.filter(account_owner=request.user.username)
    for record in records:
        if record.budget_id in budget_dict:
            record.category_display = budget_dict[record.budget_id]
    response = render(request, "Explore/records.html", context={"records": records, "budgets": budgets, "budget_select": budget_select})
    response["HX-Push-Url"] = request.path
    return response

@login_required
def edit_record(request, transaction_id):
    record = Transactions.objects.get(transaction_id=transaction_id)
    budgets = Budgets.objects.filter(username=request.user.username)
    if request.POST.get("budget_selector") == "None":
        record.budget_id = None
    else:
        record.budget_id = request.POST.get("budget_selector")
    record.save()
    category_name = "None"
    if record.budget_id:
        category_name = Budgets.objects.get(username=request.user.username, budget_id=record.budget_id).category_display
    budget_select = render_block_to_string("Explore/partials.html", "budget_select", context={"budgets": budgets})
    html = render_block_to_string("Explore/partials.html", "record", context={"record": record, "budget_select": budget_select, "category_name": category_name})
    return HttpResponse(html)

