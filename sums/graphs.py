import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
from sums.models import Budgets
import plotly.express as px
import plotly




def return_pie(username):
    labels = []
    amounts = []
    total = 0
    budgets = Budgets.objects.filter(username=username)
    for object in budgets:
        labels.append(f"{object.category_display}: ${object.monthly_budget}")
        amounts.append(object.monthly_budget)
        total += object.monthly_budget

    df = {"labels": labels, "amounts": amounts}

    fig = px.pie(df, values='amounts', names='labels', title=f'Monthly Total: ${total}')
    fig.show()
    graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div")
    return graph_div