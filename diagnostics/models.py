from django.db import models
from accounts.models import Account


class Diagnostic(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Question(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    mark1 = models.BooleanField(blank=True, default=False)
    mark2 = models.BooleanField(blank=True, default=False)
    mark3 = models.BooleanField(blank=True, default=False)
    mark4 = models.BooleanField(blank=True, default=False)


class Answer(models.Model):
    question = models.ForeignKey(Question,  on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    correct = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.title


class DiagnosticResult(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    mark1 = models.IntegerField(blank=True, null=True)
    mark2 = models.IntegerField(blank=True, null=True)
    mark3 = models.IntegerField(blank=True, null=True)
    mark4 = models.IntegerField(blank=True, null=True)