# Generated by Django 3.1.5 on 2021-02-03 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0002_servers_deploymodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servers',
            name='deploymodel',
            field=models.IntegerField(choices=[('0', '整站部署'), ('1', '部署index')], default='0'),
        ),
    ]