from django import forms
from django.shortcuts import render
from django.http import HttpResponse
import markdown2

from . import util


class EditPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50, name="title", required=True)
    content = forms.CharField(label="Content", widget=forms.Textarea, name="content")


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
        return render(request, "encyclopedia/error.html", {"title": title})


def search(request):
    if request.method == "POST":
        pages = util.list_entries()
        search = request.POST["q"].lower()
        results = [page for page in pages if search in page.lower()]

    return render(request, "encyclopedia/search.html", {"results": results})


def add_page(request):

    return render(request, "encyclopedia/add_page.html", {"form": EditPageForm()})
