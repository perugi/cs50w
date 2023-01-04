from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .constants import CATEGORY_CHOICES
from .models import Listing, User, Comment, Bid


def index(request):
    active_listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {"listings": active_listings})


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid"]
        labels = {"bid": ""}


@login_required
def bid(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: listing does not exist")

    form = BidForm(request.POST)
    if form.is_valid():
        new_bid = form.save(commit=False)
        new_bid.bidder = request.user
        new_bid.listing_id = listing_id

        if new_bid.bidder == listing.creator:
            return HttpResponseBadRequest("Cannot bid on own item")

        # This is a first bid, the bid can be equal or larger to starting bid
        if not listing.bids.exists():
            if new_bid.bid >= listing.bid:
                listing.bid = new_bid.bid
                new_bid.save()
                listing.save()
            else:
                return HttpResponseBadRequest("Input a valid bid (starting or higher)")
        # If a bid already exists, the new bid must be larger than the existing one
        else:
            if new_bid.bid > listing.bid:
                listing.bid = new_bid.bid
                new_bid.save()
                listing.save()
            else:
                return HttpResponseBadRequest(
                    "Input a valid bid (higher than the current)"
                )

    return HttpResponseRedirect(
        reverse("view_listing", kwargs={"listing_id": listing_id})
    )


def categories(request, category):
    listings = Listing.objects.filter(category=category)
    return render(
        request,
        "auctions/category.html",
        {"listings": listings, "categories": CATEGORY_CHOICES, "active": category},
    )


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": ""}


@login_required
def closed_listings(request):
    closed_listings = Listing.objects.filter(active=False)
    return render(
        request, "auctions/closed_listings.html", {"listings": closed_listings}
    )


def close_listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: listing does not exist")

    if request.user == listing.creator:
        listing.active = False
        listing.save()
    else:
        return HttpResponseBadRequest("Cannot close: you are not the listing creator")

    return HttpResponseRedirect(
        reverse("view_listing", kwargs={"listing_id": listing_id})
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


@login_required
def my_listings(request):
    listings = Listing.objects.filter(creator=request.user)
    return render(request, "auctions/my_listings.html", {"listings": listings})


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
    if request.user in listing.watchlist.all():
        listing.watchlist.remove(request.user.id)
    else:
        listing.watchlist.add(request.user.id)

    return HttpResponseRedirect(
        reverse("view_listing", kwargs={"listing_id": listing_id})
    )


def view_listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: listing does not exist")

    if request.user in listing.watchlist.all():
        watchlisted = True
    else:
        watchlisted = False

    comments = Comment.objects.filter(listing=listing)

    no_bids = len(Bid.objects.filter(listing=listing))
    highest_bid = Bid.objects.filter(listing=listing, bid=listing.bid).first()
    if highest_bid and request.user.id == highest_bid.bidder.id:
        highest = True
    else:
        highest = False

    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "watchlisted": watchlisted,
            "comments": comments,
            "comment_form": CommentForm,
            "no_bids": no_bids,
            "bid_form": BidForm,
            "highest": highest,
        },
    )


@login_required
def watchlist(request):
    watchlisted = [
        listing
        for listing in Listing.objects.all()
        if request.user in listing.watchlist.all()
    ]

    return render(request, "auctions/watchlist.html", {"listings": watchlisted})
