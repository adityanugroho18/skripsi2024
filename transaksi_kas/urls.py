from django.urls import path
from .views import *

urlpatterns = [
    path("transaksi/", index, name="transaksi_kas.index"),
    path("transaksi/create/", create, name="transaksi_kas.create"),
    path("transaksi/store/", store, name="transaksi_kas.store"),
    path("transaksi/detail/<str:kode_transaksi>", detail, name="transaksi_kas.detail"),
    path("transaksi/edit/<str:kode_transaksi>", edit, name="transaksi_kas.edit"),
    path("transaksi/update/<str:kode_transaksi>/", update, name="transaksi_kas.update"),
    path("transaksi/delete/<str:kode_transaksi>", delete, name="transaksi_kas.delete"),
    path("laporan/", laporan, name="transaksi_kas.laporan"),
    path("laporan/export-pdf", export_to_pdf, name="transaksi_kas.laporan.export_pdf"),
    path("laporan/export-excel", export_to_excel, name="transaksi_kas.laporan.export_excel"),
]
