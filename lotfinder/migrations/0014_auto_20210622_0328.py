# Generated by Django 3.1.7 on 2021-06-22 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lotfinder', '0013_booking_monthlysubscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkinglot',
            name='gmaplink',
            field=models.CharField(max_length=300),
        ),
    ]