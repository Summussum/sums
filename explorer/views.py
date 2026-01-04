from django.shortcuts import render, redirect
from django.http import HttpResponse
from render_block import render_block_to_string
from django.contrib.auth.decorators import login_required
from sums.tools import get_query_pages, get_page_links
from sums.models import Transactions, Budgets
from http import HTTPStatus
from datetime import datetime, date
from django.db.models import Sum, FloatField
import logging, json




#Initiate logging
logger = logging.getLogger(__name__)



# Create your views here.
@login_required
def index(request):
    response = render(request, "Explore/index.html", context={})
    response["HX-Push-Url"] = request.path
    return response

@login_required
def query_records(request):
    budgets = Budgets.objects.filter(user=request.user)
    budget_options = budgets.values()
    options = []
    for item in budget_options:
        item['budget_amount'] = float(item['budget_amount'])
        options.append(item)
    request.session["category_selected"] = ""
    request.session["budget_options"] = options
    request.session["records_query_string"] = ""
    records_query = Transactions.objects.filter(user=request.user)
    records = records_query.order_by('transaction_id', 'transaction_date').values('account__nickname', 'budget__category_display', 'budget__category_name', 'transaction_id', 'amount', 'transaction_date', 'transaction_description', 'budget', 'note', 'recurring', 'user', 'account')
    for item in records:
        item["transaction_date"] = item["transaction_date"].strftime('%b %d, %Y')
    records_pages = get_query_pages(records, 40)
    #logger.error(len(records_pages))
    #for record in records_pages:
        #logger.error(record)
    request.session["records_pages"] = json.dumps(records_pages)
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
    request.session["records_query_context"] = json.dumps({"dates": dates, "options": options})
    page_links = get_page_links(request, 1, "/explorer/records/")
    response = render(request, "Explore/records.html", context={"records": records_pages[0], "dates": dates, "options": options, "page_num": 1, "page_count": len(records_pages), "page_links": page_links})
    #response = render(request, "Explore/records.html", context={"records": records, "dates": dates, "options": options})
    response["HX-Push-Url"] = request.path
    #logger.error(response)
    return response

@login_required
def query1(request):
    category_name = request.POST.get("category_select")
    request.session["category_selected"] = ""
    year = request.POST.get("year")
    month = request.POST.get("month")
    query_string = f"{month}/{year}"
    if category_name != "all":
        query_string = f"{category_name} in {month}/{year}".title()
    request.session["records_query_string"] = query_string
    options = request.session["budget_options"]
    filters = {"user": request.user}
    if year != "all":
        filters["transaction_date__year"] = year
    if month != "all":
        filters["transaction_date__month"] = month
    if category_name == "uncategorized":
        filters["budget_id__isnull"] = True
    elif category_name != "all":
        filters["budget"] = Budgets.objects.filter(user=request.user, category_name=category_name).first()
        request.session["category_selected"] = filters["budget"].category_display + ",  "
    records = Transactions.objects.filter(**filters).order_by('transaction_id', 'transaction_date').values('account__nickname', 'budget__category_name', 'budget__category_display', 'transaction_id', 'amount', 'transaction_date', 'transaction_description', 'budget', 'note', 'recurring', 'user', 'account')
    for item in records:
        item["transaction_date"] = item["transaction_date"].strftime('%b %d, %Y')
    records_pages = get_query_pages(records, 40)
    request.session["records_pages"] = json.dumps(records_pages)
    page_links = get_page_links(request, 1, "/explorer/records/")
    html = render_block_to_string("Explore/partials.html", "record_table", context={"records": records_pages[0], "query_string": query_string, "options": options, "category_selected": request.session["category_selected"], "page_links": page_links}, request=request)
    #logger.error(html)
    return HttpResponse(html)

@login_required
def query2(request):
    category_name = request.POST.get("category_select")
    request.session["category_selected"] = ""
    start_date = request.POST.get("start_date")
    start_date_object = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = request.POST.get("end_date")
    end_date_object = datetime.strptime(end_date, "%Y-%m-%d")
    if category_name != "all":
        query_string = f"{category_name} in {start_date_object.strftime("%d %b %Y")} to {end_date_object.strftime("%d %b %Y")} inclusive".title()
    else:
        query_string = f"{start_date_object.strftime("%d %b %Y")} to {end_date_object.strftime("%d %b %Y")} inclusive"
    request.session["records_query_string"] = query_string
    options = request.session["budget_options"]
    filters = {"user": request.user, "transaction_date__gte": start_date, "transaction_date__lte": end_date}
    if category_name == "uncategorized":
        filters["budget_id__isnull"] = True
    elif category_name != "all":
        filters["budget"] = Budgets.objects.filter(user=request.user, category_name=category_name).first()
        request.session["category_selected"] = filters["budget"].category_display + ",  "
    records = Transactions.objects.filter(**filters).order_by('transaction_id', 'transaction_date').values('account__nickname', 'budget__category_name', 'budget__category_display', 'transaction_id', 'amount', 'transaction_date', 'transaction_description', 'budget', 'note', 'recurring', 'user', 'account')
    for item in records:
        item["transaction_date"] = item["transaction_date"].strftime('%b %d, %Y')
    records_pages = get_query_pages(records, 40)
    request.session["records_pages"] = json.dumps(records_pages)
    page_links = get_page_links(request, 1, "/explorer/records/")
    html = render_block_to_string("Explore/partials.html", "record_table", context={"records": records_pages[0], "query_string": query_string, "options": options, "category_selected": request.session["category_selected"], "page_links": page_links}, request=request)
    return HttpResponse(html)

def change_page(request, page_num):
    page = json.loads(request.session["records_pages"])[page_num-1]
    options = request.session["budget_options"]
    query_string = request.session["records_query_string"]
    page_links = get_page_links(request, page_num, "/explorer/records/")
    html = render_block_to_string("Explore/partials.html", "record_table", context={"records": page, "query_string": query_string, "options": options, "category_selected": request.session["category_selected"], "page_links": page_links}, request=request)
    return HttpResponse(html)


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
    income_budget = budgets.filter(budget_type="income").first()
    if not income_budget:
        income_budget.amount_amount = 0.00
        income_budget.category_display = "Income"
    total_budget = 0.00
    ledger = {}
    for budget in budgets:
        budget_float = float(budget.budget_amount)
        ledger[budget.category_display] = budget_float
        if budget.budget_type == "expense":
            total_budget += budget_float
    records_query = Transactions.objects.filter(user=request.user)
    years_list = records_query.dates('transaction_date', 'year')
    years = []
    for year in years_list:
        years.append(year.strftime("%Y"))
    months_list = records_query.dates('transaction_date', 'month')
    months = []
    month_strings = []
    for month in months_list:
        months.append(month.strftime("%m"))
        month_strings.append(month.strftime("%b"))
    month_strings = month_strings[::-1]
    expense_list = []
    #logger = logging.getLogger(__name__)
    #logger.error(f"First month: {months[0]}, Months List: {months}")
    for year in years[::-1]:
        for i, month in enumerate(months[::-1]):
            report = {"year": year, "month": month, "month_string": month_strings[i], "data": [], "total_expenses": 0.00, "total_diff": 0.00, "diff_color": "black", "income": {}}
            expense_query = Transactions.objects.filter(user=request.user, transaction_date__year=year, transaction_date__month=month).values("budget_id", "budget__category_display").annotate(Sum("amount"))
            if not expense_query:
                continue
            for entry in expense_query:
                subtotal = round(float(entry["amount__sum"]), 2)
                category_display = entry["budget__category_display"]
                if category_display:
                    budget_amount = ledger[category_display]
                else:
                    budget_amount = 0.00
                diff = round(subtotal + budget_amount, 2)
                diff_color = "black"
                if diff < 0:
                    diff_color = "red"
                datum = {"category_display": category_display, "budget_amount": budget_amount, "subtotal": subtotal, "diff": diff, "diff_color": diff_color}
                if entry["budget__category_display"] == None:
                    datum["category_display"] = "Uncategorized"
                    report["data"].append(datum)
                    report["total_expenses"] += subtotal
                elif budgets.get(category_display=entry["budget__category_display"]).budget_type == "expense":
                    report["data"].append(datum)
                    report["total_expenses"] += subtotal
                elif budgets.get(category_display=entry["budget__category_display"]).budget_type == "income":
                    if not report["income"]:
                        datum["diff"] = subtotal - budget_amount
                        datum["category_display"] = "Income"
                        report["income"] = datum
                    else:
                        report["income"]["subtotal"] += subtotal
                        report["income"]["budget_amount"] += budget_amount
            if report["income"]:
                report["income"]["diff_color"] = "black"
                if report["income"]["diff"] < 0:
                    report["income"]["diff_color"] = "red"
                report["income"]["diff"] = round((report["income"]["subtotal"] - report["income"]["budget_amount"]), 2)
            else:
                report["income"] = {"category_display": income_budget.category_display, "budget_amount": income_budget.budget_amount, "subtotal": 0.00, "diff": 0, "diff_color": "black"}
            report["total_expenses"] = round(report["total_expenses"], 2)
            report["total_diff"] = round((total_budget + report["total_expenses"]), 2)
            if report["total_diff"] < 0:
                report["diff_color"] = "red"
            report["balance"] = round((report["income"]["subtotal"] + report["total_expenses"]), 2)
            expense_list.append(report)
            #logger = logging.getLogger(__name__)
            #logger.error(f"report: {report}, expenses: {expense_list}")
    return render(request, "Explore/monthly_reports.html", context={"expense_list": expense_list, "total_budget": round(total_budget, 2)})

@login_required
def filter_form(request, query_select):
    if query_select == 1:
        html = render_block_to_string("Explore/partials.html", "filter_form_1", context=json.loads(request.session["records_query_context"]))
        return HttpResponse(html)
    elif query_select == 2:
        html = render_block_to_string("Explore/partials.html", "filter_form_2", context={"options": request.session["budget_options"]})
        return HttpResponse(html)
    response = HttpResponse()
    response["HX-Redirect"] = "/explorer/records/"
    return response

@login_required
def delete_record(request, record_id):
    record = Transactions.objects.get(user=request.user, transaction_id=record_id)
    if not record:
        html = render(request, "<tr><td colspan='5'>could not be deleted</td></tr>")
        response = HttpResponse(html)
        response["HX-Swap"] = "afterend"
        return HttpResponse(html)
    description = record.transaction_description
    message = f"transaction, [{record.transaction_description}] was deleted"
    record.delete()
    html = render_block_to_string("Explore/partials.html", "delete_record", request=request)
    return HttpResponse(html)


def teapot(request):
    return render(
        request,
        "Explore/teapot.html",
        status=HTTPStatus.IM_A_TEAPOT,
    )
    

