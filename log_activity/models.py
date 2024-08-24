from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class LogActivity(models.Model):
    KATEGORI_CHOICE = (
        ('master', 'Master'),
        ('transaksi', 'Transaksi'),
        ('sistem', 'Sistem'),
    )
    MASTER = 'master'
    TRANSAKSI = 'transaksi'
    SISTEM = 'sistem'

    id_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_user', null=True)
    kategori = models.CharField(max_length=10, choices=KATEGORI_CHOICE)
    keterangan = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'log_activity'  # Specify the desired table name

class LogActivityDetail(models.Model):
    JENIS_TRANSAKSI_CHOICE = (
        ('kas', 'Kas'),
        ('bank', 'Bank'),
        ('memorial', 'Memorial'),
    )
    KAS = 'kas'
    BANK = 'bank'
    MEMORIAL = 'memorial'
    TIPE_CHOICE = (
        ('create', 'Create'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
    )
    CREATE = 'create'
    EDIT = 'edit'
    DELETE = 'delete'

    id_log_activity = models.ForeignKey(LogActivity, on_delete=models.CASCADE)
    jenis_transaksi = models.CharField(max_length=8, choices=JENIS_TRANSAKSI_CHOICE)
    tipe = models.CharField(max_length=8, choices=TIPE_CHOICE)
    keterangan = models.TextField()

    class Meta:
        db_table = 'log_activity_detail'  # Specify the desired table name