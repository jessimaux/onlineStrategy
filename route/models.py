from django.db import models
from accounts.models import Account
import os


class Manual(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    TYPE_CHOICES = (
        ('КПК', 'Курс повышения квалификации'),
        ('СЕМ', 'Семинар'),
        ('МЕТ', 'Методичка')
    )
    type = models.CharField(max_length=32, choices=TYPE_CHOICES, default='КПК', verbose_name='Тип')
    link = models.CharField(max_length=1023, blank=True, null=True, verbose_name='Доступность')
    mark1 = models.PositiveIntegerField(blank=True, null=True, verbose_name='Методические компетенции')
    mark2 = models.PositiveIntegerField(blank=True, null=True, verbose_name='Функциональная грамотность')
    mark3 = models.PositiveIntegerField(blank=True, null=True, verbose_name='Психолого-педагогические компетенции')
    mark4 = models.PositiveIntegerField(blank=True, null=True, verbose_name='Предметные компетенции')


class Route(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    manual = models.ForeignKey(Manual, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('АКТИВ', 'В процессе'),
        ('ЗАКР', 'Завершен'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='АКТИВ')
    deadline = models.DateField(blank=True, null=True)
    order = models.IntegerField(default=1000)


class RouteReflection(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    STATUS_CHOICES = (
        ('СМОТР', 'На рассмотрении'),
        ('ПОДТВ', 'Подтвержден'),
        ('ОТКЛ', 'Отклонено'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='РАССМ')
    commentary = models.TextField(blank=True, null=True)


class LessonSigns(models.Model):
    teacher = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    lesson_title = models.CharField(max_length=255, blank=True, null=True)
    lesson_description = models.TextField(blank=True, null=True)
    lesson_plan = models.FileField(upload_to='files')

    def filename(self):
        return os.path.basename(self.lesson_plan.name)

    MEET_TYPE = (
        ('ДИСТ', 'Дистанционная встреча'),
        ('ОЧНО', 'Очная встреча')
    )
    meet_type = models.CharField(max_length=8, choices=MEET_TYPE, default='ОЧНО')
    meet_link = models.CharField(max_length=1023, blank=True, null=True)

    methodist_comment = models.TextField(blank=True, null=True)

    STATUS_CHOICES = (
        ('ОТКЛ', 'Отклонено'),
        ('СМОТР', 'На рассмотрении'),
        ('СОГЛ', 'Согласована'),
        ('ОТКАЗ', 'Отказ участника'),
        ('ПРОВ', 'Проведено')
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='СМОТР')