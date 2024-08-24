from django.urls import path
from .views import *

urlpatterns = [
    path("transaksi/", index, name="transaksi_bank.index"),
    path("transaksi/create/", create, name="transaksi_bank.create"),
    path("transaksi/store/", store, name="transaksi_bank.store"),
    path("transaksi/detail/<str:kode_transaksi>", detail, name="transaksi_bank.detail"),
    path("transaksi/edit/<str:kode_transaksi>", edit, name="transaksi_bank.edit"),
    path("transaksi/update/<str:kode_transaksi>/", update, name="transaksi_bank.update"),
    path("transaksi/delete/<str:kode_transaksi>", delete, name="transaksi_bank.delete"),
    path("laporan/", laporan, name="transaksi_bank.laporan"),
    path("laporan/export-pdf", export_to_pdf, name="transaksi_bank.laporan.export_pdf"),
    path("laporan/export-excel", export_to_excel, name="transaksi_bank.laporan.export_excel"),
]
