from django.db import models

# Create your models here.
class Customer(models.Model):
    nama = models.CharField(max_length=50)
    alamat = models.TextField(null=True)
    no_hp = models.CharField(unique=True, max_length=15)
    piutang = models.DecimalField(max_digits=13, decimal_places=2)

    class Meta:
        db_table = 'customer'  # Specify the desired table name