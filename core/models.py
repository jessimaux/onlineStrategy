from django.db import models
from accounts.models import Account


class Diagnostic(models.Model):
    title = models.CharField(max_length=256, blank=True)


class Question(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=256, blank=True)


class Answer(models.Model):
    question = models.ForeignKey(Question,  on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=256, blank=True)
    correct = models.BooleanField(blank=True)

    def __str__(self):
        return self.title


class DiagnosticResult(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.DO_NOTHING)
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    mark = models.IntegerField(blank=True, null=True)