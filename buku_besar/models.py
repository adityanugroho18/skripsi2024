from django.db import models

# Create your models here.
class ViewLabaRugi(models.Model):
    bulan = models.IntegerField()
    tahun = models.IntegerField()
    nominal = models.DecimalField(max_digits=15, decimal_places=2)
    kode_akun = models.CharField(max_length=255)
    kode_lawan = models.CharField(max_length=255)
    tipe = models.CharField(max_length=255)

    class Meta:
        managed = False  # No migrations will be created for this model
        db_table = 'view_laba_rugi'