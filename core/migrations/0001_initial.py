# Generated by Django 3.2.7 on 2022-03-10 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnostic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=256)),
                ('diagnostic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.diagnostic')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=256)),
                ('correct', models.BooleanField(blank=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.question')),
            ],
        ),
    ]
