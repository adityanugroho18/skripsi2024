# utils.py

from django.core.paginator import Paginator
from decimal import Decimal
from django.http.request import HttpRequest
from log_activity.models import LogActivity, LogActivityDetail
from datetime import datetime
from transaksi_kas.models import TransaksiKas
from transaksi_bank.models import TransaksiBank
from memorial.models import Memorial
from django.utils import timezone
from django.db.models import Max
import locale

def pagination(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    start_index = (page_obj.number - 1) * paginator.per_page + 1
    end_index = start_index + paginator.per_page - 1
    if end_index > paginator.count:
        end_index = paginator.count
    
    pagination_data = {
        'pagination': page_obj,
        'start_index': start_index,
        'end_index': end_index,
        'total_count': paginator.count,
    }
    
    return pagination_data

def currency_format(value):
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # Set to US locale for formatting
        formatted_value = locale.format_string("%0.2f", float(value), grouping=True)
        formatted_value = formatted_value.replace(',', 'temp').replace('.', ',').replace('temp', '.')
        return formatted_value
    except (ValueError, TypeError):
        return value

def clear_currency_format(number):
    number = number.replace('.', '')
    number = number.replace(',', '.')
    return Decimal(number)

def record_activity(
        request: HttpRequest,
        keterangan: str,
        kategori: str,
        jenis_transaksi: str = None,
        tipe: str = None,
    ):
    # Common data for LogActivity creation
    log_activity_data = {
        'id_user': request.user,
        'kategori': kategori,
    }

    if jenis_transaksi:
        # Create LogActivity
        log_activity = LogActivity.objects.create(**log_activity_data)

        # Create LogActivityDetail
        LogActivityDetail.objects.create(
            id_log_activity=log_activity,
            jenis_transaksi=jenis_transaksi,
            tipe=tipe,
            keterangan=keterangan
        )
    else:
        # If jenis_transaksi is None, include keterangan in LogActivity creation
        log_activity_data['keterangan'] = keterangan
        log_activity = LogActivity.objects.create(**log_activity_data)

def date_format(value, format_in, format_out):
    # Parse the date string 'dd-mm-yyyy' to a datetime object
    date_obj = datetime.strptime(value, format_in)

    # Convert the datetime object to 'yyyy-mm-dd' format
    date_formatted = date_obj.strftime(format_out)

    return date_formatted

def generate_transaction_code(jenis_transaksi:str, tipe:str):
    if jenis_transaksi == 'kas':
        code = 'TK' + ('M' if tipe == 'masuk' else 'K')
        mymodel = TransaksiKas
    elif jenis_transaksi == 'bank':
        code = 'TB' + ('M' if tipe == 'masuk' else 'K')
        mymodel = TransaksiBank
    else:
        code = 'TM' + ('M' if tipe == 'masuk' else 'K')
        mymodel = Memorial

    today = timezone.now().date()
    formatted_date = today.strftime('%y-%m')
    
    # Fetch the latest transaction code for today
    latest_transaction = mymodel.objects.filter(kode_transaksi__startswith=f'{code}-{formatted_date}').aggregate(Max('kode_transaksi'))
    last_code = latest_transaction['kode_transaksi__max']
    
    if last_code:
        last_serial_number = int(last_code.split('-')[-1]) + 1
    else:
        last_serial_number = 1
    
    transaction_code = f'{code}-{formatted_date}-{last_serial_number:03}'
    return transaction_code

def generate_tipe_jurnal(tipe:str):
    return ('debit' if tipe == 'masuk' else 'kredit')