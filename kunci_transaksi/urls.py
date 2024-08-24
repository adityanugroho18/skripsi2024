from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="kunci_transaksi.index"),
    path("edit/<int:id>/", edit, name="kunci_transaksi.edit"),
    path("update/<int:id>/", update, name="kunci_transaksi.update"),
]