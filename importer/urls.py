from django.urls import path

from . import views

urlpatterns = [
   path("", views.index, name="importer_index"),
   path("file_upload/", views.csv_file_upload, name="csv_file_upload"),
   path("new_account/", views.make_new_account, name="make_new_account")
]