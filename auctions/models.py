from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
   pass

class Bid(models.Model):
    bidPrice = models.DecimalField(max_digits=7,decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,default=1)


class Listing(models.Model):
    price = models.DecimalField(max_digits=7,decimal_places = 2)
    description = models.CharField(max_length=128)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE,default=1)
    lister = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    image = field_name = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    
class Comments(models.Model):
    comment = models.CharField(max_length=128)
    commentPoster = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    upVotes = models.IntegerField()
    downVotes = models.IntegerField()