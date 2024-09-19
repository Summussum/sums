from django.urls import path

from . import views

urlpatterns = [
    path("", views.sums_index, name="sums_index"),
    path("logout/", views.sums_logout, name="sums_logout"),
    path("login/", views.sums_entrypoint, name="sums_entrypoint"),
    path("login_submit/", views.sums_login_submit, name="sums_login_submit"),
    path("register_submit/", views.sums_register_submit, name="sums_register_submit"),
    path("login/login/", views.sums_login_form, name="login_form"),
    path("login/register/", views.sums_register_form, name="register_form")
]