from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.render_page, name="render_page"),
    path("search/", views.search, name="search"),
    path("add/", views.add_page, name="add_page"),
]
