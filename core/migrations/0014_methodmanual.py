# Generated by Django 3.2.7 on 2022-06-03 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_methodistlessonsigns_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='MethodManual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256, null=True)),
                ('author', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('link', models.CharField(blank=True, max_length=512, null=True)),
                ('mark1', models.IntegerField(blank=True, null=True)),
                ('mark2', models.IntegerField(blank=True, null=True)),
                ('mark3', models.IntegerField(blank=True, null=True)),
                ('mark4', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
