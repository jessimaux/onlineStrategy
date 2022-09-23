from django.db import models
from accounts.models import Account
from core.models import Municipality, Settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Methodist2Teacher(models.Model):
    methodist = models.ForeignKey(Account, related_name='methodist2teachers', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Account, related_name='teachers', on_delete=models.CASCADE)


class MethodMunicipality(models.Model):
    mun = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    method = models.ForeignKey(Account, on_delete=models.CASCADE)


if Settings.objects.get(name="auto_method_assign").value == True:
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
