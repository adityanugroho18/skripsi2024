from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Seed the database with initial group data'

    def handle(self, *args, **kwargs):
        groups = [
            {
                'name': 'staf',
            },
            {
                'name': 'atasan',
            }
        ]

        for group_data in groups:
            if not Group.objects.filter(name=group_data['name']).exists():
                Group.objects.create(**group_data)
                self.stdout.write(self.style.SUCCESS(f"Group {group_data['name']} created"))
            else:
                self.stdout.write(self.style.WARNING(f"Group {group_data['name']} already exists"))
