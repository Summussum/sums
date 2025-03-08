from django.urls import path

from . import views

urlpatterns = [
   path("", views.index, name="chronicler_index"),
   path("assign/", views.assign, name="chronicler_assign"),
   path("edit/<int:transaction_id>", views.edit, name="chronicler_edit"),
   path("new_budget/", views.new_budget, name="chronicle_new_budget")
]