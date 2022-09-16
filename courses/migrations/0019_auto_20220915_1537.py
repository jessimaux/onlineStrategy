# Generated by Django 3.2.8 on 2022-09-15 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0018_rename_accountcourse_account2course'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='account2course',
            name='role',
            field=models.CharField(choices=[('УЧ', 'Участник'), ('ЭКСП', 'Эксперт'), ('КООРД', 'Координатор')], default='УЧ', max_length=8),
        ),
        migrations.AlterField(
            model_name='account2course',
            name='status',
            field=models.CharField(choices=[('ОТКЛ', 'Отклонено'), ('СМОТР', 'На рассмотрении'), ('ОДОБР', 'Одобрено'), ('ОТКАЗ', 'Отказ участника')], default='СМОТР', max_length=8),
        ),
        migrations.AlterField(
            model_name='course',
            name='certificate',
            field=models.CharField(choices=[('УСТ', 'Установленного образца'), ('ДР', 'Другой')], default='УСТ', max_length=8),
        ),
        migrations.AlterField(
            model_name='course',
            name='profile',
            field=models.CharField(choices=[('ВСЕ', 'Все профили'), ('Предметные', 'Предметные'), ('Метапредметные', 'Метапредметные'), ('Управленческие', 'Управленческие')], default='ВСЕ', max_length=32),
        ),
        migrations.AlterField(
            model_name='course',
            name='reason',
            field=models.TextField(blank=True, max_length=1023),
        ),
        migrations.AlterField(
            model_name='course',
            name='subject',
            field=models.CharField(choices=[('ВСЕ', 'Все предметы'), ('Биология', 'Биология'), ('Математика', 'Математика')], default='ВСЕ', max_length=32),
        ),
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='course',
            name='type',
            field=models.CharField(blank=True, choices=[('КПК', 'Курс повышения квалификации'), ('СЕМ', 'Семинар')], max_length=8),
        ),
        migrations.AlterField(
            model_name='course',
            name='type_education',
            field=models.CharField(blank=True, choices=[('Б', 'Бюджет'), ('ВБ', 'Внебюджет')], max_length=8),
        ),
        migrations.AlterField(
            model_name='courseprogram',
            name='item',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='coursespeakers',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='coursespeakers',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]