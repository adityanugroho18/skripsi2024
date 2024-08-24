from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seed the database with initial user data'

    def handle(self, *args, **kwargs):
        users = [
            {
                'first_name': 'Staf',
                'last_name': 'Accounting',
                'username': 'staf',
                'email': 'staf@mail.com',
                'password': '12345678'
            },
            {
                'first_name': 'Atasan',
                'last_name': '',
                'username': 'atasan',
                'email': 'atasan@mail.com',
                'password': '12345678',
            }
        ]

        for user_data in users:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(**user_data)
                self.stdout.write(self.style.SUCCESS(f"User {user_data['username']} created"))
            else:
                self.stdout.write(self.style.WARNING(f"User {user_data['username']} already exists"))
