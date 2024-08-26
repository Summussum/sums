import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
from sums.models import Budgets
import plotly.express as px
import plotly




def return_pie():
    labels = []
    amounts = []
    budgets = Budgets.objects.all()
    for object in budgets:
        labels.append(object.category_display)
        amounts.append(object.monthly_budget)

    df = {"labels": labels, "amounts": amounts}

    fig = px.pie(df, values='amounts', names='labels', title='Budget Breakdown')
    fig.show()
    graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div")
    return graph_div