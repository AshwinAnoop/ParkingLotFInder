# Generated by Django 3.1.7 on 2021-06-01 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lotfinder', '0009_auto_20210521_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='paymentstatus',
            field=models.BooleanField(default=False),
        ),
    ]