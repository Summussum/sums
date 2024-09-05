from django.urls import path

from . import views

urlpatterns = [
   path("", views.index, name="importer_index"),
   path("file_upload/", views.csv_file_upload, name="csv_file_upload")
]