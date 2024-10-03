from django.urls import path

from . import views

urlpatterns = [
   path("", views.index, name="explorer_index"),
   path("records/", views.query_records, name="query_records"),
   path("record/<int:transaction_id>", views.edit_record, name="edit_record")
]