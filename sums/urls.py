from django.urls import path

from . import views

urlpatterns = [
    path("", views.sums_index, name="sums_index"),
    path("login_submit/", views.sums_login, name="sums_login")
]