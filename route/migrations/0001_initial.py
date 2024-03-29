# Generated by Django 3.2.8 on 2022-09-13 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Manual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256, null=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('type', models.CharField(choices=[('КПК', 'Курс повышения квалификации'), ('СЕМ', 'Семинар'), ('МЕТ', 'Методичка')], default='КПК', max_length=32, verbose_name='Тип')),
                ('link', models.CharField(blank=True, max_length=512, null=True, verbose_name='Доступность')),
                ('mark1', models.PositiveIntegerField(blank=True, null=True, verbose_name='Методические компетенции')),
                ('mark2', models.PositiveIntegerField(blank=True, null=True, verbose_name='Функциональная грамотность')),
                ('mark3', models.PositiveIntegerField(blank=True, null=True, verbose_name='Психолого-педагогические компетенции')),
                ('mark4', models.PositiveIntegerField(blank=True, null=True, verbose_name='Предметные компетенции')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('АКТИВ', 'В процессе'), ('ЗАКР', 'Завершен')], default='ПЛАН', max_length=32)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('order', models.IntegerField(default=1000)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('manual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='route.manual')),
            ],
        ),
        migrations.CreateModel(
            name='RouteReflection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('РАССМ', 'На рассмотрении'), ('ПОДТВ', 'Подтвержден'), ('ОТКЛ', 'Отклонено')], default='РАССМ', max_length=32)),
                ('commentary', models.TextField(blank=True, null=True)),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='route.route')),
            ],
        ),
        migrations.CreateModel(
            name='LessonSigns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('lesson_title', models.CharField(blank=True, max_length=256, null=True)),
                ('lesson_description', models.TextField(blank=True, null=True)),
                ('lesson_plan', models.FileField(upload_to='files')),
                ('meet_type', models.CharField(choices=[('ДИСТ', 'Дистанционная встреча'), ('ОЧНО', 'Очная встреча')], default='ОЧНО', max_length=32)),
                ('meet_link', models.CharField(blank=True, max_length=512, null=True)),
                ('methodist_comment', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('ОТКЛ', 'Отклонено'), ('СМОТР', 'На рассмотрении'), ('СОГЛОФ', 'Согласована очная встреча'), ('СОГЛОН', 'Согласована дистанционная встреча'), ('ОТКАЗ', 'Отказ участника'), ('ПРОВ', 'Проведено')], default='СМОТР', max_length=32)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
