from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="allocator_index"),
    path("create_budget_category/", views.create_budget_category, name="create_budget_category"),
    path("display_active_budget/", views.display_active_budget, name="display_active_budget"),
    path("<slug:category_name>", views.allocate, name="allocator"),
    path("reset/<slug:category_name>", views.reset, name="budget_display_reset"),
    path("error_clear/", views.error_clear, name="allocator_error_clear")
]