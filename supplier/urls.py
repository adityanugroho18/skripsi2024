from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="supplier.index"),
    path("create/", create, name="supplier.create"),
    path("store/", store, name="supplier.store"),
    path("edit/<int:id>/", edit, name="supplier.edit"),
    path("update/<int:id>/", update, name="supplier.update"),
    path("delete/<int:id>/", delete, name="supplier.delete"),
]