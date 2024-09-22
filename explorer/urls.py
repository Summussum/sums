from django.urls import path

from . import views

urlpatterns = [
   path("", views.index, name="explorer_index"),
   path("records/", views.query_records, name="query_records")
]