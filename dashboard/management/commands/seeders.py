from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run all seeders'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Running group_seeder...'))
        call_command('group_seeder')
        self.stdout.write(self.style.SUCCESS('group_seeder completed.'))

        self.stdout.write(self.style.NOTICE('Running user_seeder...'))
        call_command('user_seeder')
        self.stdout.write(self.style.SUCCESS('user_seeder completed.'))

        self.stdout.write(self.style.NOTICE('Running user_group_seeder...'))
        call_command('user_group_seeder')
        self.stdout.write(self.style.SUCCESS('user_group_seeder completed.'))

        self.stdout.write(self.style.NOTICE('Running kunci_transaksi_seeder...'))
        call_command('kunci_transaksi_seeder')
        self.stdout.write(self.style.SUCCESS('kunci_transaksi_seeder completed.'))

        self.stdout.write(self.style.SUCCESS('All seeders have been run successfully.'))
