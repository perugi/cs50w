from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .constants import CATEGORY_CHOICES
from .models import Listing, User, Comment


def index(request):
    return render(request, "auctions/index.html", {"listings": Listing.objects.all()})


def categories(request, category):
    listings = Listing.objects.filter(category=category)
    return render(
        request,
        "auctions/category.html",
        {"listings": listings, "categories": CATEGORY_CHOICES, "active": category},
    )


@login_required
def comment(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: listing does not exist")

    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.author = request.user
        new_comment.listing_id = listing_id
        new_comment.save()

    return HttpResponseRedirect(
        reverse("view_listing", kwargs={"listing_id": listing_id})
    )


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "bid", "description", "image", "category"]
        labels = {"bid": "Starting bid"}


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.creator = request.user
            new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {"form": ListingForm()})


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


@login_required
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def set_watchlist(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: listing does not exist")
    if request.user.id in [user.id for user in listing.watchlist.all()]:
        listing.watchlist.remove(request.user.id)
    else:
        listing.watchlist.add(request.user.id)

    return HttpResponseRedirect(
        reverse("view_listing", kwargs={"listing_id": listing_id})
    )


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": "New comment"}


def view_listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: listing does not exist")

    if request.user.id in [user.id for user in listing.watchlist.all()]:
        watchlisted = True
    else:
        watchlisted = False

    comments = Comment.objects.filter(listing=listing)

    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "watchlisted": watchlisted,
            "comments": comments,
            "comment_form": CommentForm,
        },
    )


@login_required
def watchlist(request):
    watchlisted = [
        listing
        for listing in Listing.objects.all()
        if request.user.id in [user.id for user in listing.watchlist.all()]
    ]
    return render(request, "auctions/watchlist.html", {"listings": watchlisted})
