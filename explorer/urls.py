from django.urls import path

from . import views

urlpatterns = [
   path("", views.index, name="explorer_index"),
   path("records/", views.query_records, name="query_records"),
   path("record/<int:transaction_id>", views.edit_record, name="edit_record"),
   path("reports/", views.monthly_reports, name="explorer_monthly_reports"),
   path("graphs/", views.teapot, name="explorer_graphs"),
   path("trends/", views.teapot, name="explorer_trends"),
   path("progress/", views.teapot, name="explorer_progress"),
   path("query1/", views.query1, name="records_query1"),
   path("query2/", views.query2, name="records_query2"),
   path("filter_form/<int:query_select>", views.filter_form, name="explorer_filter_form"),
   path("records/<int:page_num>", views.change_page, name="records_change_page")
]
