from django.urls import path

from . import views

urlpatterns = [
   path("", views.index, name="chronicler_index"),
   path("assign/", views.assign, name="chronicler_assign"),
   path("edit/<int:transaction_id>", views.edit, name="chronicler_edit")
]