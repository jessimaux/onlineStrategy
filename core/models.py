from django.db import models
from accounts.models import Account
import os

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields

from django.db.models.signals import post_save
from django.dispatch import receiver


class Diagnostic(models.Model):
    title = models.CharField(max_length=256, blank=True)


class Question(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=256, blank=True)
    mark1 = models.BooleanField(blank=True, default=False)
    mark2 = models.BooleanField(blank=True, default=False)
    mark3 = models.BooleanField(blank=True, default=False)
    mark4 = models.BooleanField(blank=True, default=False)


class Answer(models.Model):
    question = models.ForeignKey(Question,  on_delete=models.DO_NOTHING)
    ans = models.CharField(max_length=256, blank=True)
    correct = models.BooleanField(blank=True)

    def __str__(self):
        return self.ans


class DiagnosticResult(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.DO_NOTHING)
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    mark1 = models.IntegerField(blank=True, null=True)
    mark2 = models.IntegerField(blank=True, null=True)
    mark3 = models.IntegerField(blank=True, null=True)
    mark4 = models.IntegerField(blank=True, null=True)


class Methodist2Teacher(models.Model):
    methodist = models.ForeignKey(Account, related_name='methodist2teachers', on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Account, related_name='teachers', on_delete=models.DO_NOTHING)


class MethodistLessonSigns(models.Model):
    teacher = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    lesson_title = models.CharField(max_length=256, blank=True, null=True)
    lesson_description = models.TextField(blank=True, null=True)
    lesson_plan = models.FileField(upload_to='files')

    def filename(self):
        return os.path.basename(self.lesson_plan.name)

    MEET_TYPE = (
        ('ДИСТ', 'Дистанционная встреча'),
        ('ОЧНО', 'Очная встреча')
    )
    meet_type = models.CharField(max_length=32, choices=MEET_TYPE, default='ОЧНО')
    meet_link = models.CharField(max_length=512, blank=True, null=True)

    methodist_comment = models.TextField(blank=True, null=True)

    STATUS_CHOICES = (
        ('ОТКЛ', 'Отклонено'),
        ('СМОТР', 'На рассмотрении'),
        ('СОГЛОФ', 'Согласована очная встреча'),
        ('СОГЛОН', 'Согласована дистанционная встреча'),
        ('ОТКАЗ', 'Отказ участника'),
        ('ПРОВ', 'Проведено')
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='СМОТР')


class RouteManual(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    TYPE_CHOICES = (
        ('КПК', 'Курс повышения квалификации'),
        ('СЕМ', 'Семинар'),
        ('МЕТ', 'Методичка')
    )
    type = models.CharField(max_length=32, choices=TYPE_CHOICES, default='КПК', verbose_name='Тип')
    link = models.CharField(max_length=512, blank=True, null=True, verbose_name='Доступность')
    mark1 = models.PositiveIntegerField(blank=True, null=True, verbose_name='Методические компетенции')
    mark2 = models.PositiveIntegerField(blank=True, null=True, verbose_name='Функциональная грамотность')
    mark3 = models.PositiveIntegerField(blank=True, null=True, verbose_name='Психолого-педагогические компетенции')
    mark4 = models.PositiveIntegerField(blank=True, null=True, verbose_name='Предметные компетенции')


class Route(models.Model):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    manual = models.ForeignKey(RouteManual, on_delete=models.DO_NOTHING)
    STATUS_CHOICES = (
        ('АКТИВ', 'В процессе'),
        ('ЗАКР', 'Завершен'),
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='ПЛАН')
    deadline = models.DateField(blank=True, null=True)
    reflection = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=1000)


class Events(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey('content_type', 'object_id')

    EVENT_TYPE_CHOICES = (
        ('EDIT', 'Редактировано'),
        ('DEL', 'Удалено'),
        ('CREATE', ' Создано')
    )
    event_type = models.CharField(max_length=32, choices=EVENT_TYPE_CHOICES, blank=True, null=True)


class EventEditedFields(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    fields = models.CharField(max_length=256, blank=True, null=True)
    prev = models.CharField(max_length=256, blank=True, null=True)
    current = models.CharField(max_length=256, blank=True, null=True)


class Municipality(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name


class MethodMunicipality(models.Model):
    mun = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    method = models.ForeignKey(Account, on_delete=models.CASCADE)


@receiver(post_save, sender=Account)
def my_handler(sender, **kwargs):
    try:
        methodist_acc = Methodist2Teacher.objects.get(teacher_id=kwargs['instance'].id)
    except Methodist2Teacher.DoesNotExist:
        municipality = kwargs['instance'].municipality
        methodist_list = MethodMunicipality.objects.filter(mun=municipality)

        min_teacher_count = float("inf")
        methodist_acc = None
        for methodist in methodist_list:
            teacher_count = len(Methodist2Teacher.objects.filter(methodist_id=methodist.method_id))
            if teacher_count <= min_teacher_count:
                min_teacher_count = teacher_count
                methodist_acc = methodist.method

        obj = Methodist2Teacher(methodist=methodist_acc, teacher=kwargs['instance'])
        obj.save()
