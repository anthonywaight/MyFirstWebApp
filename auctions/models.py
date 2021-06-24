from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
   pass

class Bid(models.Model):
    bidPrice = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,default=1)


class Listing(models.Model):
    price = models.IntegerField()
    description = models.CharField(max_length=128)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE,default=1)
    lister = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    

