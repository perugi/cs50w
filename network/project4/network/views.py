from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Textarea

from .models import User, Post


# @login_required
# def new_post(request):
#     if request.method == "POST":
#         form = ListingForm(request.POST)
#         if form.is_valid():
#             new_listing = form.save(commit=False)
#             new_listing.creator = request.user
#             new_listing.save()
#         return HttpResponseRedirect(reverse("index"))
#     else:
#         return render(request, "auctions/create.html", {"form": ListingForm()})


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        labels = {"content": ""}
        widgets = {"content": Textarea(attrs={"class": "form-control"})}


@login_required
def follow(request, profile_id):
    try:
        profile = User.objects.get(pk=profile_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: user does not exist")

    if request.user in profile.followers.all():
        profile.followers.remove(request.user.id)
    else:
        profile.followers.add(request.user.id)

    return HttpResponseRedirect(
        reverse("view_profile", kwargs={"profile_id": profile_id})
    )


@login_required
def following(request):
    posts = Post.objects.filter().order_by("-timestamp")
    return render(
        request, "network/following.html", {"posts": posts, "new_post": PostForm()}
    )


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    return render(
        request, "network/index.html", {"posts": posts, "new_post": PostForm()}
    )


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
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.creator = request.user
            new_post.save()
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
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def view_profile(request, profile_id):
    try:
        profile = User.objects.get(pk=profile_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: user does not exist")

    no_followers = len(profile.followers.all())
    no_following = len(profile.following.all())

    # Not logged in or viewing own profile.
    if not request.user.id or request.user == profile:
        following = None
    # Else, check if the logged in user is following the viewed profile.
    elif request.user in profile.followers.all():
        following = True
    else:
        following = False

    print(f"following: {following}")
    posts = profile.posts.all().order_by("-timestamp")

    return render(
        request,
        "network/profile.html",
        {
            "profile": profile,
            "no_followers": no_followers,
            "no_following": no_following,
            "following": following,
            "posts": posts,
        },
    )
