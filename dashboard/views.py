from django.shortcuts import render
import os
from pathlib import Path
from django.contrib import messages
from datetime import datetime
from transaksi_kas.models import TransaksiKas
from transaksi_bank.models import TransaksiBank
from django.db.models import Sum
from django.conf import settings

# Create your views here.
context = {
    'app_name': os.environ.get('APP_NAME', settings.APP_NAME)
}

def index(request):
    context['title'] = 'Dashboard'
    current_month = datetime.now().month
    current_month_name = datetime.now()
    current_month_name = current_month_name.strftime('%B')
    current_year = datetime.now().year
    context['month'] = current_month
    context['month_name'] = current_month_name
    context['year'] = current_year
    try:
        kas_masuk = TransaksiKas.objects.filter(
            tanggal__month=current_month,
            tanggal__year=current_year,
            tipe='masuk'
        ).aggregate(total=Sum('total'))['total']
        kas_keluar = TransaksiKas.objects.filter(
            tanggal__month=current_month,
            tanggal__year=current_year,
            tipe='keluar'
        ).aggregate(total=Sum('total'))['total']
        bank_masuk = TransaksiBank.objects.filter(
            tanggal__month=current_month,
            tanggal__year=current_year,
            tipe='masuk'
        ).aggregate(total=Sum('total'))['total']
        bank_keluar = TransaksiBank.objects.filter(
            tanggal__month=current_month,
            tanggal__year=current_year,
            tipe='keluar'
        ).aggregate(total=Sum('total'))['total']
        context['kas_masuk'] = (0 if kas_masuk == None else kas_masuk)
        context['kas_keluar'] = (0 if kas_keluar == None else kas_keluar)
        context['bank_masuk'] = (0 if bank_masuk == None else bank_masuk)
        context['bank_keluar'] = (0 if bank_keluar == None else bank_keluar)

        context['kas'] = TransaksiKas.objects.filter(
            tanggal__month=current_month,
            tanggal__year=current_year
        ).select_related('kode_akun').order_by('-tanggal')[:5]
        context['bank'] = TransaksiBank.objects.filter(
            tanggal__month=current_month,
            tanggal__year=current_year
        ).select_related('kode_akun').order_by('-tanggal')[:5]
    except Exception as e:
        messages.warning(request, str(e))

    return render(request, 'dashboard/index.html', context)