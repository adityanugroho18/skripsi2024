from django.urls import path
from .views import *

urlpatterns = [
    path("buku-besar", index, name="buku_besar.index"),
    path("buku-besar/export-excel", export_to_excel, name="buku_besar.export_excel"),
    path("neraca-saldo", index_neraca, name="neraca_saldo.index"),
    path("neraca-saldo/export-excel", export_to_excel_neraca, name="neraca_saldo.export_excel"),
    path("laba-rugi", index_laba_rugi, name="laba_rugi.index"),
    path("laba-rugi/export-excel", export_to_excel_laba_rugi, name="laba_rugi.export_excel"),
]
