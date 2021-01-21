# Generated by Django 2.1.8 on 2021-01-11 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Servers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servername', models.CharField(max_length=200)),
                ('ip', models.GenericIPAddressField()),
                ('serveruser', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
    ]