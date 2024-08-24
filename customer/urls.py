from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="customer.index"),
    path("create/", create, name="customer.create"),
    path("store/", store, name="customer.store"),
    path("edit/<int:id>/", edit, name="customer.edit"),
    path("update/<int:id>/", update, name="customer.update"),
    path("delete/<int:id>/", delete, name="customer.delete"),
]