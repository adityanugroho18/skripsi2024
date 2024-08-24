# myapp/middleware.py

from django.shortcuts import redirect
from django.urls import reverse
import re

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that require authentication
        auth_required_urls = [
            '/dashboard/',
            '/users/',
            '/customer/',
            '/supplier/',
            '/master-akuntansi/',
            '/kas/',
            '/bank/',
            '/memorial/',
            '/user-activity/',
            '/general-ledger/',
            '/profile/',
        ]

        # Redirect authenticated users accessing the login page
        if (request.path == reverse('login') or request.path == reverse('root')) and request.user.is_authenticated:
            previous_url = request.session.get('previous_url')
            if previous_url:
                del request.session['previous_url']  # Optional: Clear the stored URL
                return redirect(previous_url)
            return redirect(reverse('dashboard'))  # Redirect to dashboard or any other page

        # Check if the requested path requires authentication
        for url_path in auth_required_urls:
            if re.match(rf'^{url_path}', request.path):
                if not request.user.is_authenticated:
                    return redirect(reverse('login'))  # Redirect to the login page

        response = self.get_response(request)
        return response
