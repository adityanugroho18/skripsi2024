from django.db import models
from kode_induk import models as KodeIndukModel

# Create your models here.
class KodeAkun(models.Model):
    class Tipe(models.TextChoices):
        DEBIT = 'debit', 'Debit'
        KREDIT = 'kredit', 'Kredit'

    TIPE_ENUM = ['debit', 'kredit']

    kode_akun = models.CharField(primary_key=True, max_length=10)
    kode_induk = models.ForeignKey(KodeIndukModel.KodeInduk, on_delete=models.CASCADE)
    nama = models.CharField(max_length=50)
    tipe = models.CharField(max_length=6, choices=Tipe.choices)

    class Meta:
        db_table = 'kode_akun'  # Specify the desired table name