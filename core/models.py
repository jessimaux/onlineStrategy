from django.db import models
from accounts.models import Account


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
    methodist_comment = models.TextField(blank=True, null=True)

    STATUS_CHOICES = (
        ('ОТКЛ', 'Отклонено'),
        ('СМОТР', 'На рассмотрении'),
        ('ОДОБР', 'Одобрено'),
        ('ОТКАЗ', 'Отказ участника'),
        ('ПРОВ', 'Проведено')
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='СМОТР')