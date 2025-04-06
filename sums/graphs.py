import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
from sums.models import Budgets
import plotly.express as px
import plotly




def return_pie(user_id):
    labels = []
    amounts = []
    total = 0
    budgets = Budgets.objects.filter(user_id=user_id)
    for object in budgets:
        labels.append(f"{object.category_display}: ${object.budget_amount}")
        amounts.append(object.budget_amount)
        total += object.budget_amount

    df = {"labels": labels, "amounts": amounts}

    fig = px.pie(df, values='amounts', names='labels', title=f'Monthly Total: ${total}')
    fig.show()
    graph_div = plotly.offline.plot(fig, auto_open = False, output_type="div")
    return graph_div