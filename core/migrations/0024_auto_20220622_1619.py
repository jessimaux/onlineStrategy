# Generated by Django 3.2.7 on 2022-06-22 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_rename_event_id_eventeditedfields_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventeditedfields',
            name='c_state',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='eventeditedfields',
            name='prev_state',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]