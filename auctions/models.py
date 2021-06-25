from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
   pass

class Bid(models.Model):
    user = models.CharField(default=None,max_length=64)
    title = models.CharField(default=None,max_length=64)
    listingid = models.IntegerField(default=None)
    bid = models.IntegerField(default=None)


class Listing(models.Model):
    seller = models.CharField(default=None,max_length=64)
    title = models.CharField(default=None,max_length=64)
    description = models.TextField(default=None)
    starting_bid = models.IntegerField(default=None)
    category = models.CharField(default=None,max_length=64)
    image_link = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #listingImage = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    
class Comments(models.Model):
    user = models.CharField(default=None,max_length=64)
    comment = models.CharField(default=None,max_length=64)
    listingid = models.IntegerField(default=None)
    timestamp = models.DateTimeField(auto_now_add=True)