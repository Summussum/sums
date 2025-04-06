from django.shortcuts import render
from django.http import HttpResponse
from render_block import render_block_to_string
from django.contrib.auth.decorators import login_required
from sums.models import Transactions, Budgets
from http import HTTPStatus
from datetime import datetime, date
from django.db.models import Sum, FloatField
import logging



# Create your views here.
@login_required
def index(request):
    budgets = Budgets.objects.filter(user=request.user)
    budget_dict = {}
    for budget in budgets:
        budget_dict[budget.budget_id] = (budget.category_name, budget.category_display)
    response = render(request, "Explore/index.html", context={"budget_select": str(budget_dict)})
    response["HX-Push-Url"] = request.path
    return response

@login_required
def query_records(request):
    budgets = Budgets.objects.filter(user=request.user)
    budget_options = budgets.values()
    options = []
    for item in budget_options:
        if item['monthly_budget'] is not None:
            item['monthly_budget'] = float(item['monthly_budget'])
        if item['annual_budget'] is not None:
            item['annual_budget'] = float(item['annual_budget'])
        options.append(item)
    request.session["budget_options"] = options
    records_query = Transactions.objects.filter(user=request.user)
    records = records_query.values('account__nickname', 'budget__category_display', 'budget__category_name', 'transaction_id', 'amount', 'transaction_date', 'transaction_description', 'budget', 'note', 'recurring', 'user', 'account')
    years_list = records_query.dates('transaction_date', 'year')
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
    options = request.session["budget_options"]
    budgets = Budgets.objects.filter(user=request.user)
    budget_select = render_block_to_string("Explore/partials.html", "budget_select", context={"budgets": budgets})
    records = Transactions.objects.filter(user=request.user, transaction_date__month=month, transaction_date__year=year).values('account__nickname', 'budget__category_name', 'budget__category_display', 'transaction_id', 'amount', 'transaction_date', 'transaction_description', 'budget', 'note', 'recurring', 'user', 'account')
    html = render_block_to_string("Explore/partials.html", "record_table", context={"budget_select": budget_select, "records": records, "query_string": query_string, "options": options}, request=request)
    return HttpResponse(html)

def query2(request):
    pass

@login_required
def edit_record(request, transaction_id):
    record = Transactions.objects.get(transaction_id=transaction_id)
    options = request.session["budget_options"]
    if request.POST.get("category_name") == "None":
        record.budget = None
    else:
        record.budget = Budgets.objects.get(user=request.user, category_name=request.POST.get("category_name"))
    record.save()
    record.budget__category_display = "None"
    record.budget__category_name = "None"
    record.account__nickname = record.account.nickname
    if record.budget:
        record.budget__category_display = record.budget.category_display
        record.budget__category_name = record.budget.category_name
    html = render_block_to_string("Explore/partials.html", "record", context={"record": record, "options": options}, request=request)
    return HttpResponse(html)

@login_required
def monthly_reports(request):
    budgets = Budgets.objects.filter(user=request.user)
    total_budget = 0.00
    ledger = {}
    for budget in budgets:
        budget_float = float(budget.monthly_budget)
        ledger[budget.category_display] = budget_float
        total_budget += budget_float
    records_query = Transactions.objects.filter(user=request.user)
    years_list = records_query.dates('transaction_date', 'year')
    years = []
    for year in years_list:
        years.append(year.strftime("%Y"))
    months_list = records_query.dates('transaction_date', 'month')
    months = []
    for month in months_list:
        months.append(month.strftime("%m"))
    expense_list = []
    #logger = logging.getLogger(__name__)
    #logger.error(f"First month: {months[0]}, Months List: {months}")
    for year in years:
        for month in months:
            report = {"year": year, "month": month, "data": [], "total_expenses": 0.00, "total_diff": 0.00, "diff_color": "black"}
            expense_query = Transactions.objects.filter(user=request.user, transaction_date__year=year, transaction_date__month=month).values("budget_id", "budget__category_display").annotate(Sum("amount"))
            if not expense_query:
                continue
            for entry in expense_query:
                datum = {}
                subtotal = round(float(entry["amount__sum"]), 2)
                datum["category_display"] = entry["budget__category_display"]
                if entry["budget__category_display"]:
                    datum["budget_amount"] = ledger[entry["budget__category_display"]]
                else:
                    datum["budget_amount"] = 0.00
                datum["subtotal"] = subtotal
                datum["diff"] = subtotal + datum["budget_amount"]
                datum["diff_color"] = "black"
                if datum["diff"] < 0:
                    datum["diff_color"] = "red"
                report["data"].append(datum)
                report["total_expenses"] += subtotal
            report["total_expenses"] = round(report["total_expenses"], 2)
            report["total_diff"] = round((total_budget + report["total_expenses"]), 2)
            if report["total_diff"] < 0:
                report["diff_color"] = "red"
            expense_list.append(report)
            #logger = logging.getLogger(__name__)
            #logger.error(f"report: {report}, expenses: {expense_list}")
    return render(request, "Explore/monthly_reports.html", context={"expense_list": expense_list, "total_budget": round(total_budget, 2)})


def teapot(request):
    return render(
        request,
        "Explore/teapot.html",
        status=HTTPStatus.IM_A_TEAPOT,
    )
    

