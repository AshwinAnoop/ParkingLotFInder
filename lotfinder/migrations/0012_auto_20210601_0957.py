# Generated by Django 3.1.7 on 2021-06-01 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lotfinder', '0011_parkinglot_bookedstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='payment',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='vacate',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
