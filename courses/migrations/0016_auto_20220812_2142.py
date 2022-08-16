# Generated by Django 3.2.8 on 2022-08-12 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_alter_course_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='audience',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='certificate',
            field=models.CharField(choices=[('УСТ', 'Установленного образца'), ('ДР', 'Другой')], default='УСТ', max_length=256),
        ),
        migrations.AlterField(
            model_name='course',
            name='profile',
            field=models.CharField(choices=[('', 'Все профили'), ('Предметные', 'Предметные'), ('Метапредметные', 'Метапредметные'), ('Управленческие', 'Управленческие')], default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='course',
            name='subject',
            field=models.CharField(choices=[('', 'Все предметы'), ('Биология', 'Биология'), ('Математика', 'Математика')], default='', max_length=256),
        ),
    ]
