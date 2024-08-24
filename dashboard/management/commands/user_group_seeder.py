from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Seed the database with initial user group data'

    def handle(self, *args, **kwargs):
        # Get users
        staf = User.objects.get(username='staf')
        atasan = User.objects.get(username='atasan')

        # Get groups
        staf_group = Group.objects.get(name='staf')
        atasan_group = Group.objects.get(name='atasan')

        # Add user to group
        staf.groups.add(staf_group)
        atasan.groups.add(atasan_group)

        # Save changes
        staf.save()
        atasan.save()

        self.stdout.write(self.style.SUCCESS(f"User successfully assigned to group"))
