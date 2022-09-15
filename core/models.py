from django.db import models
from accounts.models import Account
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields


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
    fields = models.CharField(max_length=255, blank=True, null=True)
    prev = models.CharField(max_length=255, blank=True, null=True)
    current = models.CharField(max_length=255, blank=True, null=True)


class Municipality(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name