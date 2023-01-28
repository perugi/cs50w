import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Textarea
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from .models import User, Post

from .helpers import prepare_post_page


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

POST_PER_PAGE = 10


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        labels = {"content": ""}
        widgets = {"content": Textarea(attrs={"class": "form-control", "rows": "3"})}


@csrf_exempt
@login_required
def edit_post(request):

    # Editing a post must be via PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    data = json.loads(request.body)
    id, new_content = (data["id"], data["new_content"])

    # Get the post from the db, return error if the post does not exist.
    try:
        post = Post.objects.get(pk=id)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Post does not exist"}, status=404)

    # Check that the logged in user is editing his own posts.
    if request.user.id != post.creator.id:
        return JsonResponse(
            {"message": "Cannot edit post, logged in user not the post creator."},
            status=401,
        )

    post.content = new_content
    post.edited = True
    post.timestamp = datetime.now()
    post.save()
    return JsonResponse({"message": "Post edited successfully"}, status=200)


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
        reverse("view_profile", kwargs={"profile_id": profile_id, "page": 1})
    )


@login_required
def following(request, page):
    following = User.objects.get(pk=request.user.id).following.all()
    posts = Post.objects.filter(creator__in=following)
    posts_page, pn = prepare_post_page(posts, page, POST_PER_PAGE)
    return render(
        request,
        "network/following.html",
        {"posts": posts_page, "new_post": PostForm(), "pn": pn},
    )


def index(request):
    return HttpResponseRedirect(reverse("posts", kwargs={"page": 1}))


@csrf_exempt
@login_required
def like_post(request):

    # Liking a post must be via PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    data = json.loads(request.body)
    id, new_status = (data["id"], data["new_status"])

    # Get the post from the db, return error if the post does not exist.
    try:
        post = Post.objects.get(pk=id)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Post does not exist."}, status=404)

    # Check that the new_status of the post matches what we have in the db.
    if request.user in post.likes.all():
        if new_status == True:
            return JsonResponse(
                {"message": "Like validation failed (new_status does not match db)."},
                status=409,
            )

        # Remove the users like from the db.
        post.likes.remove(request.user)
        post.no_likes -= 1
        post.save()
        return JsonResponse({"message": "Post unliked successfully"}, status=200)

    else:
        if new_status == False:
            return JsonResponse(
                {"message": "Like validation failed (new_status does not match db)."},
                status=409,
            )

        # Add the users like to the db.
        post.likes.add(request.user)
        post.no_likes += 1
        post.save()
        return JsonResponse({"message": "Post liked successfully"}, status=200)


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


def posts(request, page):
    posts = Post.objects.all()
    posts_page, pn = prepare_post_page(posts, page, POST_PER_PAGE)
    return render(
        request,
        "network/index.html",
        {
            "posts": posts_page,
            "new_post": PostForm(),
            "pn": pn,
        },
    )


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


def view_profile(request, profile_id, page):
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

    posts = profile.posts.all().order_by("-timestamp")
    posts_page, pn = prepare_post_page(posts, page, POST_PER_PAGE)

    return render(
        request,
        "network/profile.html",
        {
            "profile": profile,
            "no_followers": no_followers,
            "no_following": no_following,
            "following": following,
            "posts": posts_page,
            "pn": pn,
        },
    )
