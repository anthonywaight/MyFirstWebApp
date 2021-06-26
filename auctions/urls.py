from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createListing, name="createListing"),
    path("checkListing<str:product_id>", views.checkListing, name="checkListing"),
    path("activeListing", views.activeListing, name="activeListing")
]
