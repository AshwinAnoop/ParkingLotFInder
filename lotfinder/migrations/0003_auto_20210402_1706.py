# Generated by Django 3.1.7 on 2021-04-02 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lotfinder', '0002_parkinglot'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkinglot',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parkinglot',
            name='userid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
