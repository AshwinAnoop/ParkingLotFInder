from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class extendeduser(models.Model):
    mobile = models.CharField(max_length = 15)
    is_valet = models.BooleanField(default=False)
    walletbalance = models.IntegerField()
    user = models.OneToOneField(User,on_delete=models.CASCADE) 

    def __str__(self):
        return "{} : {}".format(self.user.id, self.user.first_name)

class parkinglot(models.Model):
    locality = models.CharField(max_length = 30)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    price = models.IntegerField()
    monthlyrent = models.BooleanField(default=False)
    userid = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to = 'pics/')
    gmaplink = models.CharField(max_length = 300)
    verifystatus = models.BooleanField(default=False)
    activestatus = models.BooleanField(default=True)
    bookedstatus = models.BooleanField(default=False)

    def __str__(self):
        return "{} : {}".format(str(self.id), self.title)

class locality(models.Model):
    locality = models.CharField(max_length = 30)

    def __str__(self):
        return self.locality

class booking(models.Model):
    lotid = models.ForeignKey(parkinglot , on_delete=models.DO_NOTHING)
    booktime = models.DateTimeField()
    vacate = models.DateTimeField(default=None, blank=True, null=True)
    userid = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    payment = models.IntegerField(default=None, blank=True, null=True)
    paymentstatus = models.BooleanField(default=False)
    valetbooking = models.BooleanField(default=False)
    monthlysubscribe = models.BooleanField(default=False)

    def __str__(self):
        return self.id

class lotverification(models.Model):
    verifier = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    verifydate = models.DateTimeField(default=None, blank=True, null=True)
    feedback = models.TextField(default=None, blank=True, null=True)
    lotid = models.ForeignKey(parkinglot , on_delete=models.DO_NOTHING)
    allotedstatus = models.BooleanField(default=True)

    def __str__(self):
        return self.id



class valet(models.Model):
    bookingid = models.ForeignKey(booking , on_delete=models.DO_NOTHING)
    valetid = models.ForeignKey(User , on_delete=models.DO_NOTHING)

class wallet(models.Model):
    userid = models.ForeignKey(User , on_delete=models.DO_NOTHING)
    amount = models.IntegerField()
    Transactdate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.id
