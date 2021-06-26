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

# view for showing the active lisitngs
@login_required(login_url='/login')
def activeListing(request):
    # list of products available
    products = Listing.objects.all()
    # checking if there are any products
    empty = False
    if len(products) == 0:
        empty = True
    return render(request, "auctions/activeListing.html", {
        "products": products,
        "empty": empty
    })


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
            item.image_link = None
        
        # saving the data into the database
        item.save()
        products = Listing.objects.all()
        empty = False
        if len(products) == 0:
            empty = True
        return render(request, "auctions/activeListing.html", {
            "products": products,
            "empty": empty
        })
    # if request is get
    else:
        return render(request,"auctions/createListing.html")

@login_required(login_url='/login')
def checkListing(request, product_id):
    # if the user submits his bid
    comments = Comments.objects.filter(listingid=product_id)

    if request.method == "POST":
        item = Listing.objects.get(id=product_id)
        newbid = int(request.POST.get('newbid'))
        #checking if the newbid is greater than or equal to current bid
        if item.starting_bid >= newbid:
            product = Listing.objects.get(id=product_id)
            return render(request, "auctions/checklisting.html", {
                "product": product,
                "message": "Your Bid should be higher than the Current one.",
                "msg_type": "danger",
                "comments": comments
            })
    
         #if bid is greater then updating in Listings table
        else:
            item.starting_bid = newbid
            item.save()
            # saving the bid in Bid model
            bidobj = Bid.objects.filter(listingid=product_id)
            if bidobj:
                bidobj.delete()
            obj = Bid()
            obj.user = request.user.username
            obj.title = item.title
            obj.listingid = product_id
            obj.bid = newbid
            obj.save()
            product = Listing.objects.get(id=product_id)
            return render(request, "auctions/checkListing.html", {
                "product": product,
                 "message": "Your Bid is added.",
                "msg_type": "success",
                "comments": comments
            })
    # accessing individual listing GET
    else:
        product = Listing.objects.get(id=product_id)
        #added = Watchlist.objects.filter(listingid=product_id, user=request.user.username)
        return render(request, "auctions/checkListing.html", {
            "product": product,
            #"added": added,
            #"comments": comments
        })