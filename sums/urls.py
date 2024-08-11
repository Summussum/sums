from django.urls import path

from . import views

urlpatterns = [
    path("", views.sums_index, name="sums_index"),
]