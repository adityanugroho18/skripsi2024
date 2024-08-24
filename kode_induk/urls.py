from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="kode_induk.index"),
    path("create/", create, name="kode_induk.create"),
    path("store/", store, name="kode_induk.store"),
    path("edit/<str:kode_induk>/", edit, name="kode_induk.edit"),
    path("update/<str:kode_induk>/", update, name="kode_induk.update"),
    path("delete/<str:kode_induk>/", delete, name="kode_induk.delete"),
]