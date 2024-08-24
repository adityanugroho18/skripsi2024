from django.shortcuts import render, redirect
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from dashboard.utils import record_activity
from log_activity.models import LogActivity
from django.contrib.auth import update_session_auth_hash

# Create your views here.
context = {
    'app_name': os.environ.get('APP_NAME', settings.APP_NAME)
}
def index(request):
    context['title'] = 'Profil'
    context['profil'] = request.user

    return render(request, 'profil/index.html', context)

def save(request):
    try:
        current = request.user
        form = request.POST
        first_name = form.get('first_name', None)
        last_name = form.get('last_name', None)
        username = form.get('username', None)
        email = form.get('email', None)

        if username != current.username and User.objects.filter(username=username).exists():
            raise ValueError('Username telah digunakan')
        if email != current.email and User.objects.filter(email=email).exists():
            raise ValueError('Email telah digunakan')
        
        user = User.objects.get(id=current.id)
        with transaction.atomic():
            if user:
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                # Record log ativity
                record_activity(request, 'Memperbarui profil', kategori=LogActivity.SISTEM)

                messages.success(request, 'Berhasil memperbarui profil')

    except ValueError as ve:
            messages.warning(request, str(ve))
    
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {e}')

    return redirect('/profile')

def change_password(request):
    context['title'] = 'Ubah Password'
    
    return render(request, 'profil/change-password.html', context)

def save_password(request):
    try:
        user = User.objects.get(id=request.user.id)
        form = request.POST
        old_password = form.get('old_password', None)
        password_new = form.get('password_new', None)
        password_conf = form.get('password_conf', None)

        if len(old_password) < 8 or len(password_new) < 8 or len(password_conf) < 8:
            raise ValueError('Password harus minimal 8 karakter')

        if not user.check_password(old_password):
            raise ValueError('Password saat ini tidak sesuai')
        if password_new != password_conf:
            raise ValueError('Konfirmasi password tidak sesuai')

        with transaction.atomic():
            if user:
                user.set_password(password_new)
                user.save()
                update_session_auth_hash(request, user)

                # Record log ativity
                record_activity(request, 'Mengubah password', kategori=LogActivity.SISTEM)

                messages.success(request, 'Berhasil memperbarui password')

    except ValueError as ve:
        messages.warning(request, str(ve))

    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {e}')

    return redirect('/profile/change-password')
