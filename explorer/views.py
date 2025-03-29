from django.shortcuts import render
from django.http import HttpResponse
from render_block import render_block_to_string
from django.contrib.auth.decorators import login_required
from sums.models import Transactions, Budgets
from http import HTTPStatus
from datetime import datetime, date



# Create your views here.
@login_required
def index(request):
    budgets = Budgets.objects.filter(user_id=request.user.id)
    budget_dict = {}
    for budget in budgets:
        budget_dict[budget.budget_id] = (budget.category_name, budget.category_display)
    response = render(request, "Explore/index.html", context={"budget_select": str(budget_dict)})
    response["HX-Push-Url"] = request.path
    return response

@login_required
def query_records(request):
    budgets = Budgets.objects.filter(user_id=request.user.id)
    budget_options = budgets.values()
    options = []
    for item in budget_options:
        if item['monthly_budget'] is not None:
            item['monthly_budget'] = float(item['monthly_budget'])
        if item['annual_budget'] is not None:
            item['annual_budget'] = float(item['annual_budget'])
        options.append(item)
    request.session["budget_options"] = options
    budget_dict = {}
    for budget in budgets:
        budget_dict[budget.budget_id] = [budget.category_display, budget.category_name]
    records = Transactions.objects.filter(user_id=request.user.id)
    for record in records:
        if record.budget_id in budget_dict:
            record.category_display = budget_dict[record.budget_id][0]
            record.category_name = budget_dict[record.budget_id][1]
    years_list = Transactions.objects.dates('transaction_date', 'year')
    years = []
    for year in years_list:
        years.append(year.strftime("%Y"))
    dates = {"current_year": datetime.now().strftime("%Y"),
               "previous_year": str(int(datetime.now().strftime("%Y"))-1).zfill(4),
               "current_month": datetime.now().strftime("%m"),
               "previous_month": str(int(datetime.now().strftime("%m"))-1).zfill(2),
               "years": years
               }
    response = render(request, "Explore/records.html", context={"records": records, "dates": dates, "options": options})
    response["HX-Push-Url"] = request.path
    return response

@login_required
def query1(request):
    year = request.POST.get("year")
    month = request.POST.get("month")
    query_string = f"{month}/{year}"
    budgets = Budgets.objects.filter(user_id=request.user.id)
    budget_dict = {}
    options = request.session["budget_options"]
    for budget in budgets:
        budget_dict[budget.budget_id] = budget.category_display
    budget_select = render_block_to_string("Explore/partials.html", "budget_select", context={"budgets": budgets})
    records = Transactions.objects.filter(user_id=request.user.id, transaction_date__month=month, transaction_date__year=year)
    for record in records:
        if record.budget_id in budget_dict:
            record.category_display = budget_dict[record.budget_id]
    html = render_block_to_string("Explore/partials.html", "record_table", context={"budget_select": budget_select, "records": records, "query_string": query_string, "options": options}, request=request)
    return HttpResponse(html)

def query2(request):
    pass

@login_required
def edit_record(request, transaction_id):
    record = Transactions.objects.get(transaction_id=transaction_id)
    options = request.session["budget_options"]
    if request.POST.get("category_name") == "None":
        record.budget_id = None
    else:
        record.budget_id = Budgets.objects.get(user_id=request.user.id, category_name=request.POST.get("category_name")).budget_id
    record.save()
    record.category_display = "None"
    record.category_name = "None"
    if record.budget_id:
        budget_item = Budgets.objects.get(user_id=request.user.id, budget_id=record.budget_id)
        record.category_display = budget_item.category_display
        record.category_name = budget_item.category_name
    html = render_block_to_string("Explore/partials.html", "record", context={"record": record, "options": options})
    return HttpResponse(html)


def teapot(request):
    return render(
        request,
        "Explore/teapot.html",
        status=HTTPStatus.IM_A_TEAPOT,
    )
    

