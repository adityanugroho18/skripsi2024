from django.shortcuts import render, redirect, get_object_or_404
from dashboard.utils import pagination, clear_currency_format, record_activity, generate_transaction_code, currency_format, generate_tipe_jurnal
from log_activity.models import LogActivity, LogActivityDetail
import os
from django.conf import settings
from django.contrib import messages
from .models import TransaksiKas, TransaksiKasDetail
from dashboard.models import Jurnal
from django.db.models import Q
from django.db import transaction
from kode_akun.models import KodeAkun
from datetime import datetime
from django.http import HttpResponse
import pandas as pd
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

# Create your views here.
context = {
    'app_name': os.environ.get('APP_NAME', settings.APP_NAME)
}

create_view = 'kas/transaksi/create.html'
edit_view = 'kas/transaksi/edit.html'
detail_view = 'kas/transaksi/detail.html'

def index(request):
    context['title'] = 'List Transaksi Kas'
    query = request.GET.get('q')
    context['query'] = query

    if query:
        kas_list = TransaksiKas.objects.filter(
            Q(kode_transaksi__icontains=query) | Q(tipe__icontains=query) | Q(total__icontains=query)
        ).select_related('kode_akun')
    else:
        kas_list = TransaksiKas.objects.all().select_related('kode_akun')

    pagination_data = pagination(request, kas_list, per_page=10)

    context['pagination'] = pagination_data['pagination']
    context['start_index'] = pagination_data['start_index']
    context['end_index'] = pagination_data['end_index']
    context['total_count'] = pagination_data['total_count']

    return render(request, 'kas/transaksi/index.html', context)

def create(request):
    context['title'] = 'Tambah Transaksi Kas'
    context['tipe'] = [TransaksiKas.MASUK, TransaksiKas.KELUAR]
    context['kode_akun'] = KodeAkun.objects.filter(
        Q(nama__icontains='Kas')
    ).select_related('kode_induk')
    context['kode_lawan'] = KodeAkun.objects.filter(
        ~Q(nama__icontains='Kas') & ~Q(nama__icontains='Bank')
    ).select_related('kode_induk')

    return render(request, create_view, context)

def store(request):
    if request.method == 'POST':
        try:
            # Get form values
            form = request.POST
            context['fieldValues'] = form
            tanggal = form['tanggal']
            tipe = form['tipe']
            kode_akun = form['kode_akun']
            total = clear_currency_format(form['total'])
            total_formated = form['total']
            kode_transaksi = generate_transaction_code('kas', tipe)
            d_nominal = form.getlist('d_nominal[]')
            d_ket = form.getlist('d_ket[]')
            d_kode_lawan = form.getlist('d_kode_lawan[]')

            with transaction.atomic():
                # Store to transaksi_kas table
                kas = TransaksiKas.objects.create(
                    kode_transaksi=kode_transaksi,
                    tanggal=tanggal,
                    tipe=tipe,
                    total=total,
                    kode_akun_id=kode_akun
                )

                # Loop detail items
                for i, val in enumerate(d_nominal):
                    # Store to transaksi_kas_detail table
                    d_nominal_val = clear_currency_format(val)
                    d_ket_val = d_ket[i]
                    d_kode_lawan_val = d_kode_lawan[i]

                    detail = TransaksiKasDetail.objects.create(
                        kode_transaksi_id=kas.kode_transaksi,
                        total=d_nominal_val,
                        keterangan=d_ket_val,
                        kode_lawan_id=d_kode_lawan_val
                    )

                    # Store to jurnal table
                    jurnal = Jurnal.objects.create(
                        tanggal=tanggal,
                        kode_transaksi=kas.kode_transaksi,
                        jenis_transaksi=Jurnal.KAS,
                        tipe=generate_tipe_jurnal(tipe),
                        kode_akun=kode_akun,
                        kode_lawan=d_kode_lawan_val,
                        nominal=d_nominal_val,
                        keterangan=d_ket_val,
                        id_transaksi=detail.id
                    )

                # Record log activity
                record_activity(
                    request,
                    f"Menambahkan data transaksi kas dengan kode '{kode_transaksi}' dan total '{total_formated}'",
                    kategori=LogActivity.TRANSAKSI,
                    jenis_transaksi=LogActivityDetail.KAS,
                    tipe=LogActivityDetail.CREATE
                )

                messages.success(request, 'Berhasil menyimpan data')
                del context['fieldValues']
                return redirect('/kas/transaksi/')

        except ValueError as ve:
            messages.warning(request, str(ve))

        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {e}')

        return redirect('/kas/transaksi/create')
    return redirect('/kas/transaksi/create')

def detail(request, kode_transaksi):
    context['title'] = 'Rincian Transaksi Kas'
    context['tipe'] = [TransaksiKas.MASUK, TransaksiKas.KELUAR]
    context['kode_akun'] = KodeAkun.objects.filter(
        Q(nama__icontains='Kas')
    ).select_related('kode_induk')
    context['kode_lawan'] = KodeAkun.objects.filter(
        ~Q(nama__icontains='Kas') & ~Q(nama__icontains='Bank')
    ).select_related('kode_induk')
    context['transaksi'] = TransaksiKas.objects.filter(kode_transaksi=kode_transaksi).select_related('kode_akun').first()
    detail_list = TransaksiKasDetail.objects.filter(kode_transaksi=kode_transaksi).select_related('kode_lawan')
    pagination_data = pagination(request, detail_list, per_page=10)

    context['pagination'] = pagination_data['pagination']
    context['start_index'] = pagination_data['start_index']
    context['end_index'] = pagination_data['end_index']
    context['total_count'] = pagination_data['total_count']

    return render(request, detail_view, context)

def edit(request, kode_transaksi:str):
    context['title'] = 'Edit Transaksi Kas'
    context['tipe'] = [TransaksiKas.MASUK, TransaksiKas.KELUAR]
    context['kode_akun'] = KodeAkun.objects.filter(
        Q(nama__icontains='Kas')
    ).select_related('kode_induk')
    context['kode_lawan'] = KodeAkun.objects.filter(
        ~Q(nama__icontains='Kas') & ~Q(nama__icontains='Bank')
    ).select_related('kode_induk')
    context['transaksi'] = get_object_or_404(TransaksiKas, kode_transaksi=kode_transaksi)
    context['detail'] = TransaksiKasDetail.objects.filter(kode_transaksi_id=kode_transaksi)

    return render(request, edit_view, context)

def update(request, kode_transaksi):
    if request.method == 'POST':
        try:
            # Get form values
            form = request.POST
            context['fieldValues'] = form
            tanggal = form['tanggal']
            tipe = form['tipe']
            kode_akun = form['kode_akun']
            total = form['total']
            total_formated = currency_format(form['total'])
            d_id = form.getlist('d_id[]')
            d_nominal = form.getlist('d_nominal[]')
            d_ket = form.getlist('d_ket[]')
            d_kode_lawan = form.getlist('d_kode_lawan[]')

            current = TransaksiKas.objects.get(kode_transaksi=kode_transaksi)
            current_detail = TransaksiKasDetail.objects.filter(kode_transaksi_id=kode_transaksi)

            with transaction.atomic():
                # Update transaksi_kas table
                current.tanggal = tanggal
                current.tipe = tipe
                current.total = total
                current.kode_akun_id = kode_akun
                current.save()

                # Delete old detail and jurnal
                for item in current_detail:
                    if str(item.id) not in d_id:
                        detail_old = TransaksiKasDetail.objects.filter(id=item.id).first()
                        if detail_old:
                            detail_old.delete()
                        jurnal_old = Jurnal.objects.filter(id_transaksi=item.id).first()
                        if jurnal_old:
                            jurnal_old.delete()

                # Loop detail items
                for i, detail_id in enumerate(d_id):
                    detail_id = int(detail_id)
                    d_nominal_val = clear_currency_format(d_nominal[i])
                    d_ket_val = d_ket[i]
                    d_kode_lawan_val = d_kode_lawan[i]

                    if detail_id == 0:
                        # Store to transaksi_kas_detail table
                        detail = TransaksiKasDetail.objects.create(
                            kode_transaksi_id=current.kode_transaksi,
                            total=d_nominal_val,
                            keterangan=d_ket_val,
                            kode_lawan_id=d_kode_lawan_val
                        )
                        # Store jurnal table
                        jurnal = Jurnal.objects.create(
                            tanggal=tanggal,
                            kode_transaksi=current.kode_transaksi,
                            jenis_transaksi=Jurnal.KAS,
                            tipe=generate_tipe_jurnal(tipe),
                            kode_akun=kode_akun,
                            kode_lawan=d_kode_lawan_val,
                            nominal=d_nominal_val,
                            keterangan=d_ket_val,
                            id_transaksi=detail.id
                        )
                    else:
                        # Update transaksi_kas_detail table if have a changes
                        detail = TransaksiKasDetail.objects.filter(id=detail_id).first()
                        if detail:
                            detail.total = d_nominal_val
                            detail.keterangan = d_ket_val
                            detail.kode_lawan_id = d_kode_lawan_val
                            detail.save()

                        # Update jurnal table if have a changes
                        jurnal = Jurnal.objects.filter(id_transaksi=detail_id).first()
                        if jurnal:
                            jurnal.tanggal = tanggal
                            jurnal.tipe = generate_tipe_jurnal(tipe)
                            jurnal.kode_akun = kode_akun
                            jurnal.kode_lawan = d_kode_lawan_val
                            jurnal.nominal = d_nominal_val
                            jurnal.keterangan = d_ket_val
                            jurnal.save()

                # Record log activity
                record_activity(
                    request,
                    f"Memperbarui data transaksi kas dengan kode '{kode_transaksi}' dan total '{total_formated}'",
                    kategori=LogActivity.TRANSAKSI,
                    jenis_transaksi=LogActivityDetail.KAS,
                    tipe=LogActivityDetail.CREATE
                )

                messages.success(request, 'Berhasil menyimpan data')
                del context['fieldValues']
                return redirect('/kas/transaksi/')

        except ValueError as ve:
            messages.warning(request, str(ve))

        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {e}')

        return redirect('/kas/transaksi/edit/'+kode_transaksi)
    return redirect('/kas/transaksi/edit/'+kode_transaksi)

def delete(request, kode_transaksi):
    try:
        # Retrieve the transaksi kas object to be deleted
        kas = get_object_or_404(TransaksiKas, kode_transaksi=kode_transaksi)

        if request.method == 'POST':
            with transaction.atomic():
                # Perform delete operation
                kas.delete()

                # Delete the jurnal
                jurnal = Jurnal.objects.get(kode_transaksi=kode_transaksi)
                if jurnal:
                    jurnal.delete()

                # Record log ativity
                record_activity(request, 'Menghapus data transaksi kas', kategori=LogActivity.TRANSAKSI)

                messages.success(request, 'Berhasil menghapus data.')
                return redirect('/kas/transaksi')

        messages.warning(request, 'Terjadi kesalahan')
        return redirect('/kas/transaksi')

    except TransaksiKas.DoesNotExist:
        messages.warning(request, 'Transaksi kas tidak ditemukan.')
        return redirect('/kas/transaksi')

    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {e}')
        return redirect('/kas/transaksi')

    except ValueError as ve:
        messages.warning(request, str(ve))


def laporan(request):
    context['title'] = 'Laporan Kas'
    context['kode_akun'] = KodeAkun.objects.filter(
        Q(nama__icontains='Kas')
    ).select_related('kode_induk')

    if request.method == 'GET':
        try:
            laporan_list = []
            form = request.GET
            context['fieldValues'] = form
            kode_akun = form.get('kode_akun', None)
            dari = form.get('dari', None)
            sampai = form.get('sampai', None)

            if kode_akun:
                # Convert dari and sampai to datetime objects
                if dari and sampai:
                    try:
                        dari = datetime.strptime(dari, '%Y-%m-%d')
                        sampai = datetime.strptime(sampai, '%Y-%m-%d')
                    except ValueError:
                        # Handle invalid date format
                        dari = None
                        sampai = None
                laporan_list = TransaksiKasDetail.objects.filter(
                    kode_transaksi__kode_akun=kode_akun,
                    kode_transaksi__tanggal__range=(dari, sampai)
                ).select_related('kode_transaksi')

            pagination_data = pagination(request, laporan_list, per_page=10)

            context['pagination'] = pagination_data['pagination']
            context['start_index'] = pagination_data['start_index']
            context['end_index'] = pagination_data['end_index']
            context['total_count'] = pagination_data['total_count']

        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'kas/laporan/index.html', context)

def export_to_pdf(request):
    kode_akun = request.GET.get('kode_akun', None)
    dari = request.GET.get('dari', None)
    sampai = request.GET.get('sampai', None)
    filename = f"Laporan Kas Periode {dari} sd {sampai}.pdf"

    # Convert dari and sampai to datetime objects
    if dari and sampai:
        try:
            dari = datetime.strptime(dari, '%Y-%m-%d')
            sampai = datetime.strptime(sampai, '%Y-%m-%d')
        except ValueError:
            dari = None
            sampai = None

    if kode_akun and dari and sampai:
        laporan = TransaksiKasDetail.objects.filter(
            kode_transaksi__kode_akun=kode_akun,
            kode_transaksi__tanggal__range=(dari, sampai)
        ).select_related('kode_transaksi')
    elif kode_akun:
        laporan = TransaksiKasDetail.objects.filter(
            kode_transaksi__kode_akun=kode_akun
        ).select_related('kode_transaksi')
    else:
        laporan = TransaksiKasDetail.objects.all().select_related('kode_transaksi')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []

    # Title
    title_style = ParagraphStyle(
        name='title',
        fontSize=18,
        leading=22,
        alignment=1,  # Center alignment
        spaceAfter=20  # Space after title
    )
    title = Paragraph(filename, title_style)
    elements.append(title)

    # Spacer to add space between title and table
    elements.append(Spacer(1, 5))

    # Table header
    data = [
        ["Kode Transaksi", "Tanggal", "Keterangan", "Pasangan", "Penerimaan", "Pengeluaran"]
    ]

    # Table data
    for detail in laporan:
        data.append([
            detail.kode_transaksi.kode_transaksi,
            detail.kode_transaksi.tanggal.strftime('%d-%m-%Y'),
            detail.keterangan,
            detail.kode_lawan_id,
            currency_format(detail.total) if detail.kode_transaksi.tipe == 'masuk' else '-',
            currency_format(detail.total) if detail.kode_transaksi.tipe == 'keluar' else '-'
        ])

    table = Table(data, colWidths=[100, 100, 150, 80, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (4, 1), (4, -1), 'RIGHT'),  # Align Penerimaan column to the right
        ('ALIGN', (5, 1), (5, -1), 'RIGHT'),  # Align Pengeluaran column to the right
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)
    return response

def export_to_excel(request):
    kode_akun = request.GET.get('kode_akun', None)
    dari = request.GET.get('dari', None)
    sampai = request.GET.get('sampai', None)
    filename = f"Laporan Kas Periode {dari} sd {sampai}.xlsx"

    # Convert dari and sampai to datetime objects
    if dari and sampai:
        try:
            dari = datetime.strptime(dari, '%Y-%m-%d')
            sampai = datetime.strptime(sampai, '%Y-%m-%d')
        except ValueError:
            dari = None
            sampai = None

    if kode_akun and dari and sampai:
        laporan = TransaksiKasDetail.objects.filter(
            kode_transaksi__kode_akun=kode_akun,
            kode_transaksi__tanggal__range=(dari, sampai)
        ).select_related('kode_transaksi')
    elif kode_akun:
        laporan = TransaksiKasDetail.objects.filter(
            kode_transaksi__kode_akun=kode_akun
        ).select_related('kode_transaksi')
    else:
        laporan = TransaksiKasDetail.objects.all().select_related('kode_transaksi')

    data = []
    for detail in laporan:
        row = {
            'Kode Transaksi': detail.kode_transaksi.kode_transaksi,
            'Tanggal': detail.kode_transaksi.tanggal,
            'Keterangan': detail.keterangan,
            'Pasangan': detail.kode_transaksi.kode_akun_id,
            'Penerimaan': (detail.total if detail.kode_transaksi.tipe == 'masuk' else '-'),
            'Pengeluaran': (detail.total if detail.kode_transaksi.tipe == 'keluar' else '-'),
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Laporan')
    
    return response