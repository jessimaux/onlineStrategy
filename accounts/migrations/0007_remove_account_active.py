# Generated by Django 3.2.7 on 2021-11-05 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20211001_1307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='active',
        ),
    ]
