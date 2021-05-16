from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class extendeduser(models.Model):
    mobile = models.CharField(max_length = 15)
    is_valet = models.BooleanField(default=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE) 

class parkinglot(models.Model):
    locality = models.CharField(max_length = 30)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    price = models.IntegerField()
    monthlyrent = models.BooleanField(default=False)
    userid = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to = 'pics/')
    gmaplink = models.CharField(max_length = 150)
    verifystatus = models.BooleanField(default=False)

class locality(models.Model):
    locality = models.CharField(max_length = 30)

class booking(models.Model):
    lotid = models.ForeignKey(parkinglot , on_delete=models.DO_NOTHING)
    booktime = models.DateTimeField()
    vacate = models.DateTimeField()
    userid = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    payment = models.IntegerField()
    valetbooking = models.BooleanField(default=False)

class lotverification(models.Model):
    verifier = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    verifydate = models.DateTimeField()
    feedback = models.TextField()
    lotid = models.ForeignKey(parkinglot , on_delete=models.DO_NOTHING)

class valet(models.Model):
    bookingid = models.ForeignKey(booking , on_delete=models.DO_NOTHING)
    valetid = models.ForeignKey(User , on_delete=models.DO_NOTHING)