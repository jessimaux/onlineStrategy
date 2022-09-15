from django.db import models
from accounts.models import Account
from model_utils import FieldTracker


class Course(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True)
    program_goal = models.TextField(blank=True)
    TYPE_CHOICES = (
        ('КПК', 'Курс повышения квалификации'),
        ('СЕМ', 'Семинар'),
    )
    type = models.CharField(max_length=8, choices=TYPE_CHOICES,blank=True)
    description = models.TextField(blank=True)
    audience = models.TextField(blank=True)
    reason = models.TextField(max_length=1023, blank=True)
    PROFILE_CHOICES = (
        ('ВСЕ', 'Все профили'),
        ('Предметные', 'Предметные'),
        ('Метапредметные', 'Метапредметные'),
        ('Управленческие', 'Управленческие'),
    )
    profile = models.CharField(max_length=32, choices=PROFILE_CHOICES, default='ВСЕ')

    SUBJECT_CHOICES = (
        ('ВСЕ', 'Все предметы'),
        ('Биология', 'Биология'),
        ('Математика', 'Математика'),
    )
    subject = models.CharField(max_length=32, choices=SUBJECT_CHOICES, default='ВСЕ')
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)
    TYPE_EDU_CHOICES = (
        ('Б', 'Бюджет'),
        ('ВБ', 'Внебюджет'),
    )
    type_education = models.CharField(max_length=8, choices=TYPE_EDU_CHOICES,blank=True)


    TYPE_CERTIFICATE = (
        ('УСТ', 'Установленного образца'),
        ('ДР', 'Другой'),
    )
    certificate = models.CharField(max_length=8, choices=TYPE_CERTIFICATE, default='УСТ')

    def __str__(self):
        return self.title


class Account2Course(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    STATUS_CHOICES = (
        ('ОТКЛ', 'Отклонено'),
        ('СМОТР', 'На рассмотрении'),
        ('ОДОБР', 'Одобрено'),
        ('ОТКАЗ', 'Отказ участника')
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='СМОТР')

    ROLE_CHOICES = (
        ('УЧ', 'Участник'),
        ('ЭКСП', 'Эксперт'),
        ('КООРД', 'Координатор'),
    )
    role = models.CharField(max_length=8, choices=ROLE_CHOICES, default='УЧ')

    reg_date = models.DateTimeField(auto_now_add=True)

    tracker = FieldTracker()


class CourseProgram(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    item = models.CharField(max_length=255, blank=True)
    duration = models.PositiveIntegerField(blank=True, null=True)


class CourseSpeakers(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)