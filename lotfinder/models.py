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
    userid = models.IntegerField()
    image = models.ImageField(upload_to = 'pics')
    gmaplink = models.CharField(max_length = 150)
    verifystatus = models.BooleanField(default=False)