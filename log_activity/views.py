from django.shortcuts import render
import os
from django.db.models import Q
from .models import LogActivity, LogActivityDetail
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from dashboard.utils import pagination
from django.db.models import OuterRef, Subquery, F, CharField, Value
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from django.db import connection

# Create your views here.
context = {
    'app_name': os.environ.get('APP_NAME', settings.APP_NAME)
}

def index(request):
    context['title'] = 'List Aktivitas User'
    query = request.GET.get('q', '')
    context['query'] = query

    sql = f"""
        SELECT activity.*, u.username, u.first_name, u.last_name, detail.jenis_transaksi, detail.tipe, detail.keterangan AS d_keterangan FROM log_activity AS activity JOIN auth_user AS u ON u.id = activity.id_user LEFT JOIN log_activity_detail AS detail ON detail.id_log_activity_id = activity.id WHERE u.first_name LIKE '%{query}%' OR u.last_name LIKE '%{query}%' OR activity.kategori LIKE '%{query}%' OR activity.keterangan LIKE '%{query}%' OR detail.keterangan LIKE '%{query}%' OR detail.jenis_transaksi LIKE '%{query}%' OR detail.tipe LIKE '%{query}%' ORDER BY activity.created_at DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(sql)
        activity_data = cursor.fetchall()

    # Convert activity_data to a list of dictionaries
    activity_list = []
    for row in activity_data:
        activity_dict = {
            'id': row[0],
            'kategori': row[1],
            'keterangan': row[2],
            'created_at': row[3],
            'id_user': row[4],
            'username': row[5],
            'first_name': row[6],
            'last_name': row[7],
            'jenis_transaksi': row[8],
            'tipe': row[9],
            'd_keterangan': row[10]
        }

        activity_list.append(activity_dict)

    pagination_data = pagination(request, activity_list, per_page=10)

    context['pagination'] = pagination_data['pagination']
    context['start_index'] = pagination_data['start_index']
    context['end_index'] = pagination_data['end_index']
    context['total_count'] = pagination_data['total_count']

    return render(request, 'log-activity/index.html', context)
