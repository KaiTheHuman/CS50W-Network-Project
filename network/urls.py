
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:page_num>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("user/<int:id>", views.user, name="user"),
    path("user/<int:id>/<int:page_num>", views.user, name="user"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("following/<int:page_num>", views.following, name="following"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("likes/<int:post_id>", views.likes, name="likes")
]