from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class extendeduser(models.Model):
    mobile = models.CharField(max_length = 15)
    is_valet = models.BooleanField(default=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE) 

