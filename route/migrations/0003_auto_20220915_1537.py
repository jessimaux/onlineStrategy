# Generated by Django 3.2.8 on 2022-09-15 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('route', '0002_auto_20220915_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='routereflection',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='lessonsigns',
            name='lesson_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lessonsigns',
            name='meet_link',
            field=models.CharField(blank=True, max_length=1023, null=True),
        ),
        migrations.AlterField(
            model_name='lessonsigns',
            name='meet_type',
            field=models.CharField(choices=[('ДИСТ', 'Дистанционная встреча'), ('ОЧНО', 'Очная встреча')], default='ОЧНО', max_length=8),
        ),
        migrations.AlterField(
            model_name='lessonsigns',
            name='status',
            field=models.CharField(choices=[('ОТКЛ', 'Отклонено'), ('СМОТР', 'На рассмотрении'), ('СОГЛ', 'Согласована'), ('ОТКАЗ', 'Отказ участника'), ('ПРОВ', 'Проведено')], default='СМОТР', max_length=8),
        ),
        migrations.AlterField(
            model_name='manual',
            name='link',
            field=models.CharField(blank=True, max_length=1023, null=True, verbose_name='Доступность'),
        ),
        migrations.AlterField(
            model_name='manual',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='route',
            name='status',
            field=models.CharField(choices=[('АКТИВ', 'В процессе'), ('ЗАКР', 'Завершен')], default='АКТИВ', max_length=8),
        ),
        migrations.AlterField(
            model_name='routereflection',
            name='status',
            field=models.CharField(choices=[('СМОТР', 'На рассмотрении'), ('ПОДТВ', 'Подтвержден'), ('ОТКЛ', 'Отклонено')], default='РАССМ', max_length=8),
        ),
    ]
