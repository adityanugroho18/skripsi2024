from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="kode_akun.index"),
    path("create/", create, name="kode_akun.create"),
    path("store/", store, name="kode_akun.store"),
    path("edit/<str:kode_akun>/", edit, name="kode_akun.edit"),
    path("update/<str:kode_akun>/", update, name="kode_akun.update"),
    path("delete/<str:kode_akun>/", delete, name="kode_akun.delete"),
]