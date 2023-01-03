from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.view_listing, name="view_listing"),
    path("set_watchlist/<int:listing_id>", views.set_watchlist, name="set_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category/<str:category>", views.categories, name="category"),
]
