from django.shortcuts import render, redirect, get_object_or_404
import os
from django.conf import settings
from .models import KodeAkun
from kode_induk.models import KodeInduk
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
create_view = 'master-akuntansi/kode-akun/create.html'
edit_view = 'master-akuntansi/kode-akun/edit.html'

def index(request):
    context['title'] = 'List Kode Akun'
    query = request.GET.get('q')
    context['query'] = query

    if query:
        kode_akun_list = KodeAkun.objects.filter(
            Q(kode_akun__icontains=query) | Q(nama__icontains=query) | Q(tipe__icontains=query)
        ).select_related('kode_induk')
    else:
        kode_akun_list = KodeAkun.objects.all().select_related('kode_induk')

    pagination_data = pagination(request, kode_akun_list, per_page=10)

    context['pagination'] = pagination_data['pagination']
    context['start_index'] = pagination_data['start_index']
    context['end_index'] = pagination_data['end_index']
    context['total_count'] = pagination_data['total_count']

    return render(request, 'master-akuntansi/kode-akun/index.html', context)

def create(request):
    context['title'] = 'Tambah Kode Akun'
    context['kode_induk'] = KodeInduk.objects.all()

    return render(request, create_view, context)

def store(request):
    context = {'title': 'Tambah Kode Akun'}
    
    if request.method == 'POST':
        form = request.POST
        context['fieldValues'] = form
        kode_akun = form['kode_akun']
        nama = form['nama']
        tipe = form['tipe']
        kode_induk = form['kode_induk']

        try:
            with transaction.atomic():
                # Max Length validation
                if len(kode_akun) > 10:
                    raise ValueError('Maksimal kode akun 10 karakter')
                if len(nama) > 50:
                    raise ValueError('Maksimal nama 50 karakter')
                if tipe not in KodeAkun.TIPE_ENUM:
                    raise ValueError('Hanya bisa memilih debit atau kredit')
                if not kode_induk:
                    raise ValueError('Harap pilih kode induk')

                # Uniqueness validation
                if KodeAkun.objects.filter(kode_akun=kode_akun, kode_induk_id=kode_induk).exists():
                    raise ValueError(f"Kode Akun '{kode_akun}' telah digunakan")

                # Create kode Akun
                kode_akun = KodeAkun.objects.create(
                    kode_akun=kode_akun,
                    nama=nama,
                    tipe=tipe,
                    kode_induk_id=kode_induk
                )

                kode_akun.save()

                # Record log ativity
                record_activity(request, 'Menambahkan data kode akun', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menyimpan data')
                del context['fieldValues']
                return redirect('/master-akuntansi/kode-akun')
        
        except ValueError as ve:
            messages.warning(request, str(ve))

        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {e}')

        return redirect('/master-akuntansi/kode-akun/create')
    return render(request, create_view, context)

def edit(request, kode_akun):
    context['title'] = 'Edit Kode Akun'
    context['kode_induk'] = KodeInduk.objects.all()
    context['kode_akun'] = get_object_or_404(KodeAkun, kode_akun=kode_akun)
    
    return render(request, edit_view, context)

def update(request, kode_akun):
    context = {'title': 'Edit Kode Akun'}
    
    try:
        current = KodeAkun.objects.get(kode_akun=kode_akun)
        context['kode_akun'] = current  # Set context here

        if request.method == 'POST':
            form = request.POST
            context['fieldValues'] = form
            new_kode_akun = form['kode_akun']
            nama = form['nama']
            tipe = form['tipe']
            kode_induk = form['kode_induk']
            
            # Max Length validation
            if len(kode_akun) > 10:
                raise ValueError('Maksimal kode akun 10 karakter')
            if len(nama) > 50:
                raise ValueError('Maksimal nama 50 karakter')
            if tipe not in KodeAkun.TIPE_ENUM:
                raise ValueError('Hanya bisa memilih debit atau kredit')
            if not kode_induk:
                raise ValueError('Harap pilih kode induk')

            # Uniqueness validation
            if new_kode_akun != current.kode_akun and KodeAkun.objects.filter(kode_akun=new_kode_akun).exists():
                raise ValueError(f"Kode Akun '{new_kode_akun}' telah digunakan")

            with transaction.atomic():
                # Update kode Akun
                with connection.cursor() as cursor:
                    sql = """
                        UPDATE kode_akun
                        SET kode_akun = %s, nama = %s, tipe = %s, kode_induk_id = %s
                        WHERE kode_akun = %s
                    """
                    cursor.execute(sql, [new_kode_akun, nama, tipe, kode_induk, kode_akun])

                # Record log ativity
                record_activity(request, 'Memperbarui data kode akun', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menyimpan data')
                del context['fieldValues']
                return redirect('/master-akuntansi/kode-akun')
        
    except KodeAkun.DoesNotExist:
        messages.warning(request, 'Data tidak ditemukan')

    except ValueError as ve:
        messages.warning(request, str(ve))

    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {e}')

    return redirect('/master-akuntansi/kode-akun/edit/'+kode_akun)

def delete(request, kode_akun):
    try:
        # Retrieve the kode Akun object to be deleted
        kode_akun = get_object_or_404(KodeAkun, kode_akun=kode_akun)

        if request.method == 'POST':
            with transaction.atomic():
                # Perform delete operation
                kode_akun.delete()

                # Record log ativity
                record_activity(request, 'Menghapus data kode akun', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menghapus data.')
                return redirect('/master-akuntansi/kode-akun')

        messages.warning(request, 'Terjadi kesalahan')
        return redirect('/master-akuntansi/kode-akun')

    except KodeAkun.DoesNotExist:
        messages.warning(request, 'Kode akun tidak ditemukan.')
        return redirect('/master-akuntansi/kode-akun')

    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {e}')
        return redirect('/master-akuntansi/kode-akun')

    except ValueError as ve:
        messages.warning(request, str(ve))