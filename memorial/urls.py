from django.urls import path
from .views import *

urlpatterns = [
    path("transaksi/", index, name="memorial.index"),
    path("transaksi/create/", create, name="memorial.create"),
    path("transaksi/store/", store, name="memorial.store"),
    path("transaksi/detail/<str:kode_transaksi>", detail, name="memorial.detail"),
    path("transaksi/edit/<str:kode_transaksi>", edit, name="memorial.edit"),
    path("transaksi/update/<str:kode_transaksi>/", update, name="memorial.update"),
    path("transaksi/delete/<str:kode_transaksi>", delete, name="memorial.delete"),
    path("laporan/", laporan, name="memorial.laporan"),
    path("laporan/export-pdf", export_to_pdf, name="memorial.laporan.export_pdf"),
    path("laporan/export-excel", export_to_excel, name="memorial.laporan.export_excel"),
]
