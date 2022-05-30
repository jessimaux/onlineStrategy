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