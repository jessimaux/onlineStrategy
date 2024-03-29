# Generated by Django 3.2.7 on 2022-01-14 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20220113_1514'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='education_organization',
            new_name='work',
        ),
        migrations.RemoveField(
            model_name='account',
            name='education_class',
        ),
        migrations.AddField(
            model_name='account',
            name='document_code_department',
            field=models.CharField(blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='account',
            name='document_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='document_department',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='account',
            name='document_number',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AddField(
            model_name='account',
            name='document_place_birth',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='account',
            name='document_serial',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AddField(
            model_name='account',
            name='education_document_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='education_document_first_name',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='account',
            name='education_document_middle_name',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='account',
            name='education_document_number',
            field=models.CharField(blank=True, max_length=7),
        ),
        migrations.AddField(
            model_name='account',
            name='education_document_reg_number',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AddField(
            model_name='account',
            name='education_document_second_name',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='account',
            name='education_document_serial',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AddField(
            model_name='account',
            name='education_level',
            field=models.CharField(blank=True, choices=[('ПР', 'Прочее'), ('СПО', 'СПО'), ('БКВТ', 'Бакалавриат'), ('СПЦ', 'Специалитет'), ('МАГ', 'Магистратура')], max_length=32),
        ),
        migrations.AddField(
            model_name='account',
            name='education_pow',
            field=models.CharField(blank=True, choices=[('Н', 'Нет степени'), ('КН', 'Кандидат наук'), ('ДОК', 'Доктор наук')], max_length=32),
        ),
        migrations.AddField(
            model_name='account',
            name='education_qualify',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='account',
            name='work_edu_exp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='work_exp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='work_pos',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
