"""
URL configuration for accounting_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Authentication
    path("", include('authentication.urls'), name="authentication"),
    # Dashboard
    path("dashboard/", include('dashboard.urls'), name="dashboard"),
    # Master Data
    path("users/", include('user.urls'), name="user"),
    path("customer/", include('customer.urls'), name="customer"),
    path("supplier/", include('supplier.urls'), name="supplier"),
    # Master Akuntansi
    path("master-akuntansi/kode-induk/", include('kode_induk.urls'), name="kode_induk"),
    path("master-akuntansi/kode-akun/", include('kode_akun.urls'), name="kode_akun"),
    path("master-akuntansi/kunci-transaksi/", include('kunci_transaksi.urls'), name="kunci_transaksi"),
    # Kas
    path("kas/", include('transaksi_kas.urls'), name="transaksi_kas"),
    # Bank
    path("bank/", include('transaksi_bank.urls'), name="transaksi_bank"),
    # Memorial
    path("memorial/", include('memorial.urls'), name="transaksi_memorial"),
    # User Activity
    path("user-activity/", include('log_activity.urls'), name="log_activity"),
    # General Ledger
    path("general-ledger/", include('buku_besar.urls'), name="general_ledger"),
    # Profile
    path("profile/", include('profil.urls'), name="profile"),
]
