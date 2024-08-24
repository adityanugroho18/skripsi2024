from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Jurnal(models.Model):
    JENIS_TRANSAKSI_CHOICE = (
        ('kas', 'Kas'),
        ('bank', 'Bank'),
        ('memorial', 'Memorial'),
    )
    KAS='kas'
    BANK='bank'
    MEMORIAL='memorial'
    TIPE_CHOICE = (
        ('debit', 'Debit'),
        ('kredit', 'Kredit'),
    )
    DEBIT='debit'
    KREDIT='kredit'

    tanggal = models.DateField()
    kode_transaksi = models.CharField(max_length=20)
    jenis_transaksi = models.CharField(max_length=8, choices=JENIS_TRANSAKSI_CHOICE)
    tipe = models.CharField(max_length=6, choices=TIPE_CHOICE)
    kode_akun = models.CharField(max_length=15)
    kode_lawan = models.CharField(max_length=15)
    nominal = models.DecimalField(max_digits=13, decimal_places=2)
    keterangan = models.TextField(null=True)
    id_transaksi = models.BigIntegerField()

    class Meta:
        db_table = 'jurnal'  # Specify the desired table name
