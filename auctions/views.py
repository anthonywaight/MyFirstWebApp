from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User
from .models import *

newListing = {}

def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def createListing(request):
    if request.method =="POST":
        item = Listing()
        item.seller = request.user.username
        item.title = request.POST.get('title')
        item.description = request.POST.get('description')
        item.category = request.POST.get('category')
        item.starting_bid = request.POST.get('starting_bid')

        if request.POST.get('image_link'):
            item.image_link = request.POST.get('image_link')
        else:
            item.image_link = "data:image/webp;base64,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"
        
        # saving the data into the database
        item.save()
        products = Listing.objects.all()
        empty = False
        if len(products) == 0:
            empty = True
        return render(request, "auctions/index.html", {
            "products": products,
            "empty": empty
        })
    else:
        return render(request,"auctions/createListing.html")
    