# Generated by Django 3.2.7 on 2022-02-04 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20220120_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='certificate',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='course',
            name='duration',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='type_education',
            field=models.CharField(blank=True, choices=[('Б', 'Бюджет'), ('ВБ', 'Внебюджет')], max_length=64),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='program_goal',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='reason',
            field=models.TextField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
