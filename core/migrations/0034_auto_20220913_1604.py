# Generated by Django 3.2.8 on 2022-09-13 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_rename_reason_routereflection_commentary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diagnosticresult',
            name='account',
        ),
        migrations.RemoveField(
            model_name='diagnosticresult',
            name='diagnostic',
        ),
        migrations.RemoveField(
            model_name='methodist2teacher',
            name='methodist',
        ),
        migrations.RemoveField(
            model_name='methodist2teacher',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='methodistlessonsigns',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='methodmunicipality',
            name='method',
        ),
        migrations.RemoveField(
            model_name='methodmunicipality',
            name='mun',
        ),
        migrations.RemoveField(
            model_name='question',
            name='diagnostic',
        ),
        migrations.RemoveField(
            model_name='route',
            name='account',
        ),
        migrations.RemoveField(
            model_name='route',
            name='manual',
        ),
        migrations.RemoveField(
            model_name='routereflection',
            name='route',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Diagnostic',
        ),
        migrations.DeleteModel(
            name='DiagnosticResult',
        ),
        migrations.DeleteModel(
            name='Methodist2Teacher',
        ),
        migrations.DeleteModel(
            name='MethodistLessonSigns',
        ),
        migrations.DeleteModel(
            name='MethodMunicipality',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Route',
        ),
        migrations.DeleteModel(
            name='RouteManual',
        ),
        migrations.DeleteModel(
            name='RouteReflection',
        ),
    ]
