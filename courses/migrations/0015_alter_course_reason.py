# Generated by Django 3.2.8 on 2022-08-09 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_rename_speaker_coursespeakers_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='reason',
            field=models.TextField(blank=True, max_length=512),
        ),
    ]