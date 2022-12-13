from django.shortcuts import render
import markdown2
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def render_page(request, title):
    content = util.get_entry(title)
    if content:
        return render(
            request,
            "encyclopedia/wiki.html",
            {"title": title, "content": markdown2.markdown(content)},
        )
    else:
        return render(
            request,
            "encyclopedia/error.html",
            {"error_message": f"Page {title} not found!"},
        )


def search(request):
    if request.method == "POST":
        pages = util.list_entries()
        search = request.POST["q"].lower()
        results = [page for page in pages if search in page.lower()]

    return render(request, "encyclopedia/search.html", {"results": results})


def add_page(request):
    if request.method == "POST":
        if request.POST["title"] not in util.list_entries():
            util.save_entry(request.POST["title"], request.POST["content"])
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "encyclopedia/error.html",
                {"error_message": f"Page {request.POST['title']} already exists!"},
            )

    return render(request, "encyclopedia/add_page.html")


def edit_page(request, title):
    if request.method == "POST":
        if title in util.list_entries():
            util.save_entry(title, request.POST["content"])
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "encyclopedia/error.html",
                {"error_message": f"Cannot edit - page {title} does not exists!"},
            )

    return render(
        request,
        "encyclopedia/edit_page.html",
        {"title": title, "content": util.get_entry(title)},
    )


def random_page(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("render_page", args=[title]))
