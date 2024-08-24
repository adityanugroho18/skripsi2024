from django.shortcuts import render, redirect, get_object_or_404
import os
from django.conf import settings
from .models import Supplier
from django.db.models import Q
from dashboard.utils import pagination, clear_currency_format, record_activity
from log_activity.models import LogActivity, LogActivityDetail
from django.contrib import messages
from django.db import transaction, connection

# Create your views here.
context = {
    'app_name': os.environ.get('APP_NAME', settings.APP_NAME)
}
create_view = 'supplier/create.html'
edit_view = 'supplier/edit.html'

def index(request):
    context['title'] = 'List Supplier'
    query = request.GET.get('q')
    context['query'] = query
    
    if query:
        supplier_list = Supplier.objects.filter(
            Q(nama__icontains=query) | Q(no_hp__icontains=query)
        )
    else:
        supplier_list = Supplier.objects.all()

    pagination_data = pagination(request, supplier_list, per_page=10)

    context['pagination'] = pagination_data['pagination']
    context['start_index'] = pagination_data['start_index']
    context['end_index'] = pagination_data['end_index']
    context['total_count'] = pagination_data['total_count']

    return render(request, 'supplier/index.html', context)

def create(request):
    context['title'] = 'Tambah Supplier'
    return render(request, create_view, context)

def store(request):
    context = {'title': 'Tambah Supplier'}
    
    if request.method == 'POST':
        form = request.POST
        context['fieldValues'] = form
        nama = form['nama']
        alamat = form['alamat']
        no_hp = form['no_hp']
        hutang = clear_currency_format(form['hutang'])

        try:
            with transaction.atomic():
                # Validate nama uniqueness
                if Supplier.objects.filter(nama=nama).exists():
                    raise ValueError('Nama telah digunakan')

                # Validate no_hp uniqueness
                if Supplier.objects.filter(no_hp=no_hp).exists():
                    raise ValueError('No handphone telah digunakan')

                # Create customer
                supplier = Supplier.objects.create(
                    nama=nama,
                    alamat=alamat,
                    no_hp=no_hp,
                    hutang=hutang,
                )
                supplier.save()

                # Record log ativity
                record_activity(request, 'Menambahkan data supplier', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menyimpan data')
                del context['fieldValues']
                return redirect('/supplier')
        
        except ValueError as ve:
            messages.warning(request, str(ve))

    return render(request, create_view, context)

def edit(request, id):
    context['title'] = 'Edit Supplier'
    context['supplier'] = get_object_or_404(Supplier, id=id)
    
    return render(request, edit_view, context)

def update(request, id):
    context = {'title': 'Edit Supplier'}
    
    if request.method == 'POST':
        form = request.POST
        context['fieldValues'] = form
        nama = form['nama']
        alamat = form['alamat']
        no_hp = form['no_hp']
        hutang = clear_currency_format(form['hutang'])

        try:
            current = Supplier.objects.get(id=id)
            with transaction.atomic():
                # Validate nama uniqueness
                if current.nama != nama and Supplier.objects.filter(nama=nama).exists():
                    raise ValueError('Nama telah digunakan')

                # Validate email uniqueness
                if current.no_hp != no_hp and no_hp and Supplier.objects.filter(no_hp=no_hp).exists():
                    raise ValueError('No handphone telah digunakan')

                # Update supplier
                current.nama = nama
                current.alamat = alamat
                current.no_hp = no_hp
                current.hutang = hutang
                current.save()

                # Record log ativity
                record_activity(request, 'Memperbarui data supplier', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menyimpan data')
                del context['fieldValues']
                return redirect('/supplier')

        except ValueError as ve:
            messages.warning(request, str(ve))

    context['supplier'] = current
    return render(request, edit_view, context)

def delete(request, id):
    try:
        # Retrieve the supplier object to be deleted
        supplier = get_object_or_404(Supplier, id=id)

        if request.method == 'POST':
            with transaction.atomic():
                # Perform delete operation
                supplier.delete()

                # Record log ativity
                record_activity(request, 'Menghapus data supplier', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menghapus data.')
                return redirect('/supplier')

        messages.warning(request, 'Terjadi kesalahan')
        return redirect('/supplier')

    except Supplier.DoesNotExist:
        messages.warning(request, 'Supplier tidak ditemukan.')
        return redirect('/supplier')

    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {e}')
        return redirect('/supplier')

    except ValueError as ve:
        messages.warning(request, str(ve))