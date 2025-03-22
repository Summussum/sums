from django.urls import path

from . import views

urlpatterns = [
   path("", views.index, name="explorer_index"),
   path("records/", views.query_records, name="query_records"),
   path("record/<int:transaction_id>", views.edit_record, name="edit_record"),
   path("graphs/", views.teapot, name="explorer_graphs"),
   path("trends/", views.teapot, name="explorer_trends"),
   path("progress/", views.teapot, name="explorer_progress"),
   path("query1/", views.query1, name="records_query1"),
   path("query2", views.query2, name="records_query2")
]
