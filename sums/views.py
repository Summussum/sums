from django.shortcuts import render

# Create your views here.
def sums_index(request):
    return render(request, "dashboard.html")