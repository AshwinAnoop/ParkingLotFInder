# Generated by Django 3.1.7 on 2021-05-16 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lotfinder', '0004_locality'),
    ]

    operations = [
        migrations.CreateModel(
            name='booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booktime', models.DateTimeField()),
                ('vacate', models.DateTimeField()),
                ('payment', models.IntegerField()),
                ('valetbooking', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='parkinglot',
            name='image',
            field=models.ImageField(upload_to='pics/'),
        ),
        migrations.AlterField(
            model_name='parkinglot',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='valet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookingid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lotfinder.booking')),
                ('valetid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='lotverification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verifydate', models.DateTimeField()),
                ('feedback', models.TextField()),
                ('lotid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lotfinder.parkinglot')),
                ('verifier', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='lotid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lotfinder.parkinglot'),
        ),
        migrations.AddField(
            model_name='booking',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]