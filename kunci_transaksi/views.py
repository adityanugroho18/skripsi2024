from django.shortcuts import render, redirect, get_object_or_404
import os
from django.conf import settings
from .models import KunciTransaksi
from dashboard.utils import record_activity, date_format
from log_activity.models import LogActivity
from django.db.models import Q
from dashboard.utils import pagination
from django.contrib import messages
from django.db import transaction

# Create your views here.
context = {
    'app_name': os.environ.get('APP_NAME', settings.APP_NAME)
}
edit_view = 'master-akuntansi/kunci-transaksi/edit.html'

def index(request):
    context['title'] = 'List Kunci Transaksi'
    query = request.GET.get('q')
    context['query'] = query

    if query:
        kunci_transaksi_list = KunciTransaksi.objects.filter(
            Q(jenis_transaksi__icontains=query)
        )
    else:
        kunci_transaksi_list = KunciTransaksi.objects.all()

    pagination_data = pagination(request, kunci_transaksi_list, per_page=10)

    context['pagination'] = pagination_data['pagination']
    context['start_index'] = pagination_data['start_index']
    context['end_index'] = pagination_data['end_index']
    context['total_count'] = pagination_data['total_count']

    return render(request, 'master-akuntansi/kunci-transaksi/index.html', context)

def edit(request, id):
    context['title'] = 'Edit Kunci Transaksi'
    context['kunci_transaksi'] = get_object_or_404(KunciTransaksi, id=id)
    # Convert date to YYYY-MM-DD format if it's not already
    if context['kunci_transaksi'].tanggal_mulai:
        context['kunci_transaksi'].tanggal_mulai = context['kunci_transaksi'].tanggal_mulai.strftime('%Y-%m-%d')
    
    return render(request, edit_view, context)

def update(request, id):
    context = {'title': 'Edit Kunci Transaksi'}
    
    try:
        current = KunciTransaksi.objects.get(id=id)
        context['kunci_transaksi'] = current  # Set context here

        if request.method == 'POST':
            form = request.POST
            context['fieldValues'] = form
            tanggal_mulai = form['tanggal_mulai']
            
            if not tanggal_mulai:
                raise ValueError('Harap tentukan tanggal mulai')

            with transaction.atomic():
                # Update kunci transaksi
                current.tanggal_mulai = tanggal_mulai
                current.save()

                # Record log ativity
                record_activity(request, 'Memperbarui data kunci transaksi', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menyimpan data')
                del context['fieldValues']
                return redirect('/master-akuntansi/kunci-transaksi')

    except ValueError as ve:
        messages.warning(request, str(ve))

    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {e}')

    return redirect('/master-akuntansi/kunci-transaksi/edit/'+str(id))