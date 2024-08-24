from django.db import models

# Create your models here.
class KodeInduk(models.Model):
    kode_induk = models.CharField(primary_key=True, max_length=10)
    nama = models.CharField(max_length=50)

    class Meta:
        db_table = 'kode_induk'  # Specify the desired table name

    def __str__(self):
        return self.kode_induk