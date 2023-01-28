from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/<int:page>", views.posts, name="posts"),
    path("new_post", views.new_post, name="new_post"),
    path(
        "profile/<int:profile_id>/<int:page>", views.view_profile, name="view_profile"
    ),
    path("follow/<int:profile_id>", views.follow, name="follow"),
    path("following/<int:page>", views.following, name="following"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("like_post", views.like_post, name="like_post"),
]
