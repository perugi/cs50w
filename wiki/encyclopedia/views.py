from django.shortcuts import render
from django.http import HttpResponse
import markdown2

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
        return render(request, "encyclopedia/error.html", {"title": title})
