# Generated by Django 3.1.5 on 2021-02-02 01:32

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Servers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('company', models.CharField(default='', max_length=200)),
                ('domain', models.CharField(default='', max_length=200)),
                ('ip', models.GenericIPAddressField(default='127.0.0.1')),
                ('serveruser', models.CharField(default='root', max_length=200)),
                ('password', models.CharField(default='', max_length=200)),
                ('region', models.CharField(default='root', max_length=200)),
                ('servername', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('icpurl', models.CharField(default='', max_length=200)),
                ('sitetitle', models.CharField(default='', max_length=200)),
                ('deploystatus', models.IntegerField(default='0')),
                ('deploytime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期')),
            ],
        ),
    ]
