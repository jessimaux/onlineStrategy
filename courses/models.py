from django.db import models
from accounts.models import Account

from django.urls import reverse_lazy

STATUS_CHOICES = (
    ('ОТКЛ', 'Отклонено'),
    ('СМОТР', 'На рассмотрении'),
    ('ОДОБР', 'Одобрено'),
    ('ОТКАЗ', 'Отказ участника')
)


class Course(models.Model):
    title = models.CharField(max_length=256, blank=True)
    program_goal = models.TextField(blank=True)
    TYPE_CHOICES = (
        ('КПК', 'Курс повышения квалификации'),
        ('СЕМ', 'Семинар'),
    )
    type = models.CharField(max_length=64, choices=TYPE_CHOICES,blank=True)
    description = models.TextField(blank=True)
    audience = models.CharField(max_length=256, blank=True)
    reason = models.TextField(max_length=256, blank=True)
    profile = models.CharField(max_length=256, default='all')
    subject = models.CharField(max_length=256, default='all')
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    TYPE_EDU_CHOICES = (
        ('Б', 'Бюджет'),
        ('ВБ', 'Внебюджет'),
    )
    type_education = models.CharField(max_length=64, choices=TYPE_EDU_CHOICES,blank=True)
    certificate = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('moderate-courses')


class AccountCourse(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='СМОТР')

    ROLE_CHOICES = (
        ('УЧ', 'Участник'),
        ('ЭКСП', 'Эксперт'),
        ('КООРД', 'Координатор'),
    )
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default='УЧ')

    reg_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return '/'


class CourseProgram(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    item = models.CharField(max_length=256, blank=True)
    duration = models.IntegerField(blank=True, null=True)


class CourseSpeakers(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=256, blank=True)