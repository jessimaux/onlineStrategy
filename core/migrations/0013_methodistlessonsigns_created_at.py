# Generated by Django 3.2.7 on 2022-06-02 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_methodistlessonsigns_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='methodistlessonsigns',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
