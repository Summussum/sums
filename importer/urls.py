from django.urls import path

from . import views

urlpatterns = [
   path("", views.index, name="importer_index"),
]