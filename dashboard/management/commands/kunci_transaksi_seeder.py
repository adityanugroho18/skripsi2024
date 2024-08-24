from django.core.management.base import BaseCommand
from kunci_transaksi.models import KunciTransaksi

class Command(BaseCommand):
    help = 'Seed the database with initial group data'

    def handle(self, *args, **kwargs):
        kunci_transaksi_data = [
            {
                'jenis_transaksi': 'Kas',
                'tanggal_mulai': '2024-07-10'
            },
            {
                'jenis_transaksi': 'Bank Memorial',
                'tanggal_mulai': '2024-07-10'
            }
        ]

        for item in kunci_transaksi_data:
            if not KunciTransaksi.objects.filter(jenis_transaksi=item['jenis_transaksi']).exists():
                KunciTransaksi.objects.create(**item)
                self.stdout.write(self.style.SUCCESS(f"Kunci transaksi {item['jenis_transaksi']} created"))
            else:
                self.stdout.write(self.style.WARNING(f"Kunci transaksi {item['jenis_transaksi']} already exists"))
