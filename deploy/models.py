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
    deployversion = models.IntegerField(choices=((0, '老版本'),
                                              (1, '新版本')),
                                     default=1,
                                     verbose_name='新版本')
    pid = models.CharField(null=False,blank=False,default='p0',max_length=200)
    iswww = models.IntegerField(choices=((0, '否'),
                                              (1, '是')),
                                     default=1,
                                     verbose_name='是否部署www')
    region = models.CharField(default='root',max_length=200)
    servername = models.UUIDField(default=uuid.uuid4, editable=False)
    icpurl=models.CharField(default='',max_length=200)
    deploymodel=models.IntegerField(choices=((0, '整站部署'),
                                              (1, '部署index')),
                                     default=0,
                                     verbose_name='部署方式')
    sitetitle = models.CharField(default='',max_length=200)
    deploystatus=models.IntegerField(choices=((0, '待部署'),
                                              (1, '已部署'),
                                              (2, '部署失败')),
                                     default=0,
                                     verbose_name='部署状态')
    deploytime=models.DateTimeField('保存日期',default = timezone.now)

    def __str__(self):
        return self.ip