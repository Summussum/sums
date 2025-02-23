from django.urls import path

from . import views

urlpatterns = [
   path("", views.index, name="chronicler_index"),
   path("assign/", views.assign, name="chronicler_assign")
]