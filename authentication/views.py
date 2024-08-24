from django.shortcuts import render, redirect
from django.views import View
import os
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.conf import settings
from log_activity.models import LogActivity, LogActivityDetail
from dashboard.utils import record_activity

# Create your views here.
class AuthenticationView(View):
    context = {
        'app_name': os.environ.get('APP_NAME', settings.APP_NAME)
    }
    def get(self, request):
        self.context['title'] = 'Login'
        return render(request, 'authentication/login.html', self.context)

    def post(self, request):
        self.context['fieldValues'] = request.POST

        # GET DATA
        username = request.POST['username']
        password = request.POST['password']

        # VALIDATE
        if not username:
            messages.warning(request, 'Username harus diisi')
            return render(request, 'authentication/login.html', self.context)
        if not password:
            messages.warning(request, 'Password harus diisi')
            return render(request, 'authentication/login.html', self.context)

        # LOGIN PROCESS
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.warning(request, 'Akun tidak ditemukan')
            return render(request, 'authentication/login.html', self.context)

        if user.check_password(password):
            user = auth.authenticate(username=username, password=password) 
            auth.login(request, user)

            # Record log activity
            record_activity(
                request,
                f"Pengguna '{user.username}' melakukan login",
                kategori=LogActivity.SISTEM
            )

            messages.success(request, 'Login berhasil')
            return redirect('dashboard')

        messages.warning(request, 'Password salah')

        return render(request, 'authentication/login.html', self.context)

class LogoutView(View):
    def post(self, request):
        # Record log activity
        record_activity(
            request,
            f"Pengguna '{request.user.username}' melakukan logout",
            kategori=LogActivity.SISTEM
        )
        auth.logout(request)
        messages.success(request, 'Successfully logout')
        return redirect('login')