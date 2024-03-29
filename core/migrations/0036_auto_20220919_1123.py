# Generated by Django 3.2.8 on 2022-09-19 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20220915_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('value', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='events',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='events',
            name='user',
        ),
        migrations.DeleteModel(
            name='EventEditedFields',
        ),
        migrations.DeleteModel(
            name='Events',
        ),
    ]
