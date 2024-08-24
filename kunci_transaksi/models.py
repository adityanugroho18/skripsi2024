from django.db import models

# Create your models here.
class KunciTransaksi(models.Model):
    JENIS_TRANSAKSI_CHOICES = (
        ('kas', 'kas'),
        ('bank memorial', 'Bank Memorial'),
    )
    jenis_transaksi = models.CharField(max_length=13, choices=JENIS_TRANSAKSI_CHOICES)
    tanggal_mulai = models.DateField()

    class Meta:
        db_table = 'kunci_transaksi'  # Specify the desired table name