# Generated by Django 3.2.7 on 2022-05-31 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_account_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='methodist',
            field=models.BooleanField(default=False),
        ),
    ]
