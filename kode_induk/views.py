from django.shortcuts import render, redirect, get_object_or_404
import os
from django.conf import settings
from .models import KodeInduk
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
create_view = 'master-akuntansi/kode-induk/create.html'
edit_view = 'master-akuntansi/kode-induk/edit.html'

def index(request):
    context['title'] = 'List Kode Induk'
    query = request.GET.get('q')
    context['query'] = query
    
    if query:
        kode_induk_list = KodeInduk.objects.filter(
            Q(kode_induk__icontains=query) | Q(nama__icontains=query)
        )
    else:
        kode_induk_list = KodeInduk.objects.all()

    pagination_data = pagination(request, kode_induk_list, per_page=10)

    context['pagination'] = pagination_data['pagination']
    context['start_index'] = pagination_data['start_index']
    context['end_index'] = pagination_data['end_index']
    context['total_count'] = pagination_data['total_count']

    return render(request, 'master-akuntansi/kode-induk/index.html', context)

def create(request):
    context['title'] = 'Tambah Kode Induk'
    return render(request, create_view, context)

def store(request):
    context = {'title': 'Tambah Kode Induk'}
    
    if request.method == 'POST':
        form = request.POST
        context['fieldValues'] = form
        kode_induk = form['kode_induk']
        nama = form['nama']

        try:
            with transaction.atomic():
                # Max Length validation
                if len(kode_induk) > 10:
                    raise ValueError('Maksimal kode induk 10 karakter')
                if len(nama) > 50:
                    raise ValueError('Maksimal nama 50 karakter')

                # Uniqueness validation
                if KodeInduk.objects.filter(kode_induk=kode_induk).exists():
                    raise ValueError(f"Kode induk '{kode_induk}' telah digunakan")

                # Create kode induk
                kode_induk = KodeInduk.objects.create(
                    kode_induk=kode_induk,
                    nama=nama
                )
                kode_induk.save()

                # Record log ativity
                record_activity(request, 'Menambahkan data kode induk', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menyimpan data')
                del context['fieldValues']
                return redirect('/master-akuntansi/kode-induk')
        
        except ValueError as ve:
            messages.warning(request, str(ve))
            return redirect('/master-akuntansi/kode-induk')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {e}')
            return redirect('/master-akuntansi/kode-induk')

    return render(request, create_view, context)

def edit(request, kode_induk):
    context['title'] = 'Edit Kode Induk'
    context['kode_induk'] = get_object_or_404(KodeInduk, kode_induk=kode_induk)
    
    return render(request, edit_view, context)

def update(request, kode_induk):
    context = {'title': 'Edit Kode Induk'}
    
    try:
        current = KodeInduk.objects.get(kode_induk=kode_induk)
        context['kode_induk'] = current  # Set context here

        if request.method == 'POST':
            form = request.POST
            context['fieldValues'] = form
            new_kode_induk = form['kode_induk']
            nama = form['nama']
            
            # Max Length validation
            if len(new_kode_induk) > 10:
                raise ValueError('Maksimal kode induk 10 karakter')
            if len(nama) > 50:
                raise ValueError('Maksimal nama 50 karakter')

            # Uniqueness validation
            if new_kode_induk != current.kode_induk and KodeInduk.objects.filter(kode_induk=new_kode_induk).exists():
                raise ValueError(f"Kode induk '{new_kode_induk}' telah digunakan")

            with transaction.atomic():
                # Update kode induk
                with connection.cursor() as cursor:
                    sql = """
                        UPDATE kode_induk
                        SET kode_induk = %s, nama = %s
                        WHERE kode_induk = %s
                    """
                    cursor.execute(sql, [new_kode_induk, nama, kode_induk])

                # Record log ativity
                record_activity(request, 'Memperbarui data kode induk', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menyimpan data')
                del context['fieldValues']
                return redirect('/master-akuntansi/kode-induk')
        
    except KodeInduk.DoesNotExist:
        messages.warning(request, 'Data tidak ditemukan')
        return redirect('/master-akuntansi/kode-induk')

    except ValueError as ve:
        messages.warning(request, str(ve))

    return redirect('/master-akuntansi/kode-induk/edit/'+kode_induk)

def delete(request, kode_induk):
    try:
        # Retrieve the kode induk object to be deleted
        kode_induk = get_object_or_404(KodeInduk, kode_induk=kode_induk)

        if request.method == 'POST':
            with transaction.atomic():
                # Perform delete operation
                kode_induk.delete()

                # Record log ativity
                record_activity(request, 'Menghapus data kode induk', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menghapus data.')
                return redirect('/master-akuntansi/kode-induk')

        messages.warning(request, 'Terjadi kesalahan')
        return redirect('/master-akuntansi/kode-induk')

    except KodeInduk.DoesNotExist:
        messages.warning(request, 'Kode induk tidak ditemukan.')
        return redirect('/master-akuntansi/kode-induk')

    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {e}')
        return redirect('/master-akuntansi/kode-induk')

    except ValueError as ve:
        messages.warning(request, str(ve))