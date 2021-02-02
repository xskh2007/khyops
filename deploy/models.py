from django.db import models
import django.utils.timezone as timezone
import uuid


# Create your models here.
class Servers(models.Model):
    id=models.AutoField(primary_key=True)
    company = models.CharField(default='',max_length=200)
    domain = models.CharField(default='',max_length=200)
    ip = models.GenericIPAddressField(default='127.0.0.1')
    serveruser = models.CharField(default='root',max_length=200)
    password = models.CharField(default='',max_length=200)
    region = models.CharField(default='root',max_length=200)
    servername = models.UUIDField(default=uuid.uuid4, editable=False)
    icpurl=models.CharField(default='',max_length=200)
    sitetitle = models.CharField(default='',max_length=200)
    deploystatus=models.IntegerField(default='0')
    deploytime=models.DateTimeField('保存日期',default = timezone.now)

    def __str__(self):
        return self.ip