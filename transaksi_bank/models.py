from django.db import models
from kode_akun import models as KodeAkunModel

# Create your models here.
class TransaksiBank(models.Model):
    TIPE_CHOICE = (
        ('masuk', 'Masuk'),
        ('keluar', 'Keluar'),
    )
    MASUK = 'masuk'
    KELUAR = 'keluar'

    kode_transaksi = models.CharField(primary_key=True, max_length=20)
    kode_akun = models.ForeignKey(KodeAkunModel.KodeAkun, on_delete=models.CASCADE)
    tanggal = models.DateField()
    tipe = models.CharField(max_length=6, choices=TIPE_CHOICE)
    total = models.DecimalField(max_digits=13, decimal_places=2)

    class Meta:
        db_table = 'transaksi_bank'  # Specify the desired table name

class TransaksiBankDetail(models.Model):
    kode_transaksi = models.ForeignKey(TransaksiBank, on_delete=models.CASCADE)
    kode_lawan = models.ForeignKey(KodeAkunModel.KodeAkun, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=13, decimal_places=2)
    keterangan = models.TextField(null=True)

    class Meta:
        db_table = 'transaksi_bank_detail'  # Specify the desired table name