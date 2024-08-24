from django.shortcuts import render, redirect, get_object_or_404
import os
from django.conf import settings
from .models import Customer
from dashboard.utils import record_activity
from log_activity.models import LogActivity, LogActivityDetail
from django.db.models import Q
from dashboard.utils import pagination, clear_currency_format
from django.contrib import messages
from django.db import transaction, connection

# Create your views here.
context = {
    'app_name': os.environ.get('APP_NAME', settings.APP_NAME)
}
create_view = 'customer/create.html'
edit_view = 'customer/edit.html'

def index(request):
    context['title'] = 'List Customer'
    query = request.GET.get('q')
    context['query'] = query
    
    if query:
        customer_list = Customer.objects.filter(
            Q(nama__icontains=query) | Q(no_hp__icontains=query)
        )
    else:
        customer_list = Customer.objects.all()

    pagination_data = pagination(request, customer_list, per_page=10)

    context['pagination'] = pagination_data['pagination']
    context['start_index'] = pagination_data['start_index']
    context['end_index'] = pagination_data['end_index']
    context['total_count'] = pagination_data['total_count']

    return render(request, 'customer/index.html', context)

def create(request):
    context['title'] = 'Tambah Customer'
    return render(request, create_view, context)

def store(request):
    context = {'title': 'Tambah Customer'}
    
    if request.method == 'POST':
        form = request.POST
        context['fieldValues'] = form
        nama = form['nama']
        alamat = form['alamat']
        no_hp = form['no_hp']
        piutang = clear_currency_format(form['piutang'])

        try:
            with transaction.atomic():
                # Validate nama uniqueness
                if Customer.objects.filter(nama=nama).exists():
                    raise ValueError('Nama telah digunakan')

                # Validate no_hp uniqueness
                if Customer.objects.filter(no_hp=no_hp).exists():
                    raise ValueError('No handphone telah digunakan')

                # Create customer
                customer = Customer.objects.create(
                    nama=nama,
                    alamat=alamat,
                    no_hp=no_hp,
                    piutang=piutang,
                )
                customer.save()

                # Record log ativity
                record_activity(request, 'Menambahkan data customer', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menyimpan data')
                del context['fieldValues']
                return redirect('/customer')
        
        except ValueError as ve:
            messages.warning(request, str(ve))

    return render(request, create_view, context)

def edit(request, id):
    context['title'] = 'Edit Customer'
    context['customer'] = get_object_or_404(Customer, id=id)
    
    return render(request, edit_view, context)

def update(request, id):
    context = {'title': 'Edit Customer'}
    
    if request.method == 'POST':
        form = request.POST
        context['fieldValues'] = form
        nama = form['nama']
        alamat = form['alamat']
        no_hp = form['no_hp']
        piutang = clear_currency_format(form['piutang'])

        try:
            current = Customer.objects.get(id=id)
            with transaction.atomic():
                # Validate nama uniqueness
                if current.nama != nama and Customer.objects.filter(nama=nama).exists():
                    raise ValueError('Nama telah digunakan')

                # Validate email uniqueness
                if current.no_hp != no_hp and no_hp and Customer.objects.filter(no_hp=no_hp).exists():
                    raise ValueError('No handphone telah digunakan')

                # Update customer
                current.nama = nama
                current.alamat = alamat
                current.no_hp = no_hp
                current.piutang = piutang
                current.save()

                # Record log ativity
                record_activity(request, 'Memperbarui data customer', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menyimpan data')
                del context['fieldValues']
                return redirect('/customer')

        except ValueError as ve:
            messages.warning(request, str(ve))

    context['customer'] = current
    return render(request, edit_view, context)

def delete(request, id):
    try:
        # Retrieve the customer object to be deleted
        customer = get_object_or_404(Customer, id=id)

        if request.method == 'POST':
            with transaction.atomic():
                # Perform delete operation
                customer.delete()

                # Record log ativity
                record_activity(request, 'Menghapus data customer', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menghapus data.')
                return redirect('/customer')

        messages.warning(request, 'Terjadi kesalahan')
        return redirect('/customer')

    except Customer.DoesNotExist:
        messages.warning(request, 'Customer tidak ditemukan.')
        return redirect('/customer')

    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {e}')
        return redirect('/customer')

    except ValueError as ve:
        messages.warning(request, str(ve))