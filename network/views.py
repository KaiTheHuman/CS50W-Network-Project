from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator

from .models import User, Post
import json


def index(request, page_num=1):
    posts = Post.objects.all().order_by("-time")
    p = Paginator(posts, 10)
    current_page=p.page(page_num)
    posts_segment = current_page.object_list
    return render(request, "network/index.html",{
        "posts":posts_segment,
        "current_page":current_page
    })


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def create(request):
    message=None
    form=NewPostForm()
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            save_post(request, content)
            return HttpResponseRedirect(reverse("index"))
        else:
            message="Invalid Input, must be below 300 characters"

    return render(request, "network/create.html", {
        "form": NewPostForm(),
        "message":message
    })

def save_post(request,content):
    post = Post(
        content=content,
        user = request.user
    )
    post.save()

def user(request,id, page_num=1):
    userpage = User.objects.get(id=id)
    posts = Post.objects.filter(user__id=id).order_by("-time")
    p = Paginator(posts, 10)
    current_page=p.page(page_num)
    posts_segment = current_page.object_list
    return render(request, "network/index.html",{
        "userpage":userpage,
        "posts":posts_segment,
        "current_page":current_page
    })

@csrf_exempt
@login_required
def follow(request, user_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        account = User.objects.get(pk= request.user.id )
        account_follow = User.objects.get(pk=user_id)
        if account == account_follow:
            return HttpResponse(status=400)
        state = data["following_state"]
        if state == "false":
            account.following.add(account_follow)
        else:
            account.following.remove(account_follow)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

@login_required
def following(request, page_num=1):
    posts = Post.objects.filter(user__in = request.user.following.all()).order_by("-time")
    p = Paginator(posts, 10)
    current_page=p.page(page_num)
    posts_segment = current_page.object_list
    return render(request, "network/index.html",{
        "posts":posts_segment,
        "current_page":current_page,
        "following": True
    })

@csrf_exempt
@login_required
def edit(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(pk=post_id)
        if post.user != request.user:
            return HttpResponse(status=403)
        content = data["content"]
        if 0< len(content) <= 300:
            post.content = content
            post.save()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=400)
    
    return HttpResponse(status=405)

@csrf_exempt
@login_required
def likes(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(pk=post_id)
        state = data["like_state"]
        if state == "false":
            post.likes_users.add(request.user)
        else:
            post.likes_users.remove(request.user)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

class NewPostForm(forms.Form):
    content = forms.CharField(label="Content", widget= forms.Textarea(), max_length=300)