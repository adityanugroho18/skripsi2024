from django.db import models
from kode_akun.models import KodeAkun

# Create your models here.
class Memorial(models.Model):
    TIPE_CHOICE = (
        ('masuk', 'Masuk'),
        ('keluar', 'Keluar'),
    )

    MASUK = 'masuk'
    KELUAR = 'keluar'

    kode_transaksi = models.CharField(primary_key=True, max_length=20)
    tanggal = models.DateField()
    tipe = models.CharField(max_length=6, choices=TIPE_CHOICE)
    total = models.DecimalField(max_digits=13, decimal_places=2)

    class Meta:
        db_table = 'memorial'  # Specify the desired table name

class MemorialDetail(models.Model):
    kode_transaksi = models.ForeignKey(Memorial, on_delete=models.CASCADE)
    kode_akun = models.ForeignKey(KodeAkun, on_delete=models.CASCADE, related_name="memorial_details_as_kode_akun")
    kode_lawan = models.ForeignKey(KodeAkun, on_delete=models.CASCADE, related_name="memorial_details_as_kode_lawan")
    total = models.DecimalField(max_digits=13, decimal_places=2)
    keterangan = models.TextField(null=True)

    class Meta:
        db_table = 'memorial_detail'  # Specify the desired table name