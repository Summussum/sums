import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
from sums.models import Budgets
import plotly.express as px
import plotly


def return_graph():

    x = np.arange(0,np.pi*3,.1)
    y = np.sin(x)

    fig = plt.figure()
    plt.plot(x,y)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


def return_pie():
    labels = []
    amounts = []
    budgets = Budgets.objects.all()
    for object in budgets:
        labels.append(object.category_name)
        amounts.append(object.monthly_budget)


    fig, ax = plt.subplots()
    ax.pie(amounts, labels=labels)

    imgdata = StringIO
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data

def return_pie2():
    labels = []
    amounts = []
    budgets = Budgets.objects.all()
    for object in budgets:
        labels.append(object.category_name)
        amounts.append(object.monthly_budget)


    plt.pie(amounts, labels=labels)

    plt.title("Budget Allocations")
    imgdata = StringIO
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data

def return_pie3():
    labels = []
    amounts = []
    budgets = Budgets.objects.all()
    for object in budgets:
        labels.append(object.category_name)
        amounts.append(object.monthly_budget)

    df = {"labels": labels, "amounts": amounts}

    fig = px.pie(df, values='amounts', names='labels', title='Budget Breakdown')
    fig.show()
    graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div")
    return graph_div