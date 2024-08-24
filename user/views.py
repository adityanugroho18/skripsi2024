from django.shortcuts import render, redirect, get_object_or_404
import os
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db.models import Q
from dashboard.utils import pagination, record_activity
from log_activity.models import LogActivity, LogActivityDetail
from django.contrib import messages
from django.db import transaction, connection, IntegrityError

# Create your views here.
context = {
    'app_name': os.environ.get('APP_NAME', settings.APP_NAME)
}
create_view = 'user/create.html'
edit_view = 'user/edit.html'

def index(request):
    context['title'] = 'List User'
    query = request.GET.get('q')
    context['query'] = query
    
    sql = """
        SELECT au.id, au.first_name, au.last_name, au.username, au.email, g.name, au.date_joined, au.last_login FROM `auth_user` AS au JOIN auth_user_groups AS ag ON ag.user_id = au.id JOIN auth_group AS g ON g.id = ag.group_id
    """
    if query:
        sql += f"""WHERE au.first_name LIKE '%%{query}%%'
                    OR au.last_name LIKE '%%{query}%%'
                    OR g.name LIKE '%%{query}%%'
                """

    with connection.cursor() as cursor:
        cursor.execute(sql)
        user_data = cursor.fetchall()

    # Convert user_data to a list of dictionaries
    user_list = []
    for row in user_data:
        user_dict = {
            'id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'username': row[3],
            'email': row[4],
            'group_name': row[5],
            'date_joined': row[6],
            'last_login': row[7],
        }
        user_list.append(user_dict)

    pagination_data = pagination(request, user_list, per_page=10)

    context['pagination'] = pagination_data['pagination']
    context['start_index'] = pagination_data['start_index']
    context['end_index'] = pagination_data['end_index']
    context['total_count'] = pagination_data['total_count']

    return render(request, 'user/index.html', context)

def create(request):
    context['title'] = 'Tambah User'
    context['groups'] = Group.objects.all()
    return render(request, create_view, context)

def store(request):
    context = {'title': 'Tambah User'}
    
    if request.method == 'POST':
        form = request.POST
        context['fieldValues'] = form
        context['groups'] = Group.objects.all()
        first_name = form['first_name']
        last_name = form['last_name']
        username = form['username']
        email = form['email']
        group_id = form['group_id']
        password = form['password']

        try:
            with transaction.atomic():
                # Validate username uniqueness
                if User.objects.filter(username=username).exists():
                    raise ValueError('Username telah digunakan')

                # Validate email uniqueness
                if email and User.objects.filter(email=email).exists():
                    raise ValueError('Email telah digunakan')

                # Validate password length
                if len(password) < 8:
                    raise ValueError('Password harus minimal 8 karakter')

                # Create user account
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.set_password(password)
                user.save()

                # Record log ativity
                record_activity(request, 'Menambahkan data user', kategori=LogActivity.MASTER)

                # Assign user group
                group = Group.objects.get(id=group_id)
                user.groups.add(group)

                messages.success(request, 'Berhasil menyimpan data')
                del context['fieldValues']
                return redirect('/users')
        
        except ValueError as ve:
            messages.warning(request, str(ve))

    return render(request, create_view, context)

def edit(request, id):
    context['title'] = 'Edit User'
    
    sql = """
        SELECT au.id, au.first_name, au.last_name, au.username, au.email, g.id, g.name, au.date_joined, au.last_login FROM `auth_user` AS au JOIN auth_user_groups AS ag ON ag.user_id = au.id JOIN auth_group AS g ON g.id = ag.group_id
        WHERE au.id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [id])
        user_data = cursor.fetchone()

    user_dict = {
        'id': user_data[0],
        'first_name': user_data[1],
        'last_name': user_data[2],
        'username': user_data[3],
        'email': user_data[4],
        'group_id': user_data[5],
        'group_name': user_data[6],
        'date_joined': user_data[7],
        'last_login': user_data[8],
    }

    context['user_data'] = user_dict
    context['groups'] = Group.objects.all()
    return render(request, edit_view, context)

def update_group(user_id, group_id):
    sql = """SELECT * FROM auth_user_groups WHERE user_id = %s"""

    with connection.cursor() as cursor:
        cursor.execute(sql, [user_id])
        group_data = cursor.fetchone()

    if group_data:
        group_dict = {
            'id': group_data[0],
            'user_id': group_data[1],
            'group_id': group_data[2]
        }
        # UPDATE
        current_auth_group_id = group_dict['id']
        current_group_id = group_dict['group_id']

        if group_id != current_group_id:
            sql = """UPDATE auth_user_groups SET group_id = %s WHERE id = %s"""
            with connection.cursor() as cursor:
                cursor.execute(sql, [group_id, current_auth_group_id])
    else:
        # CREATE
        sql = """INSERT INTO auth_user_groups VALUES(%s, %s)"""
        with connection.cursor() as cursor:
            cursor.execute(sql, [user_id, group_id]) 

def update(request, id):
    context = {'title': 'Edit User'}
    
    if request.method == 'POST':
        form = request.POST
        context['fieldValues'] = form
        context['groups'] = Group.objects.all()
        first_name = form['first_name']
        last_name = form['last_name']
        username = form['username']
        email = form['email']
        group_id = form['group_id']
        password = form['password']

        try:
            current = User.objects.get(id=id)
            with transaction.atomic():
                # Validate username uniqueness
                if current.username != username and User.objects.filter(username=username).exists():
                    raise ValueError('Username telah digunakan')

                # Validate email uniqueness
                if current.email != email and email and User.objects.filter(email=email).exists():
                    raise ValueError('Email telah digunakan')

                # Validate password length
                if password:
                    if len(password) < 8:
                        raise ValueError('Password harus minimal 8 karakter')

                # Update user account
                current.first_name = first_name
                current.last_name = last_name
                current.username = username
                current.email = email
                if password:
                    print('update password')
                    current.password = password
                current.save()

                # Adjust user group
                if group_id:
                    update_group(user_id=id, group_id=group_id)

                # Record log ativity
                record_activity(request, 'Memperbarui data user', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menyimpan data')
                del context['fieldValues']
                return redirect('/users')

        except ValueError as ve:
            messages.warning(request, str(ve))

    return render(request, edit_view, current)

def delete(request, id):
    try:
        # Retrieve the user object to be deleted
        user = get_object_or_404(User, id=id)

        if request.method == 'POST':
            with transaction.atomic():
                # Perform delete operation
                user.delete()

                # Record log ativity
                record_activity(request, 'Menghapus data user', kategori=LogActivity.MASTER)

                messages.success(request, 'Berhasil menghapus data.')
                return redirect('/users')

        messages.warning(request, 'Terjadi kesalahan')
        return redirect('/users')

    except User.DoesNotExist:
        messages.warning(request, 'User tidak ditemukan.')
        return redirect('/users')

    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {e}')
        return redirect('/users')

    except ValueError as ve:
        messages.warning(request, str(ve))