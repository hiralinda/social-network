from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import User, Post, Follow, Like
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
from .forms import BackgroundForm

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        for post in page_obj:
            post.user_liked = post.user_liked(request.user)
    else:
        for post in page_obj:
            post.user_liked = False

    return render(request, 'network/index.html', {'page_obj': page_obj})


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
def settings_view(request):
    if request.method == 'POST':
        form = BackgroundForm(request.POST)
        if form.is_valid():
            background_choice = form.cleaned_data['background_choice']
            request.user.background_choice = background_choice
            request.user.save()
            return redirect('settings')  # Redirect back to the settings page or another page
    else:
        form = BackgroundForm(initial={'background_choice': request.user.background_choice})
    
    return render(request, 'network/settings.html', {'form': form})

def new_post(request):
    if request.method == 'POST':
        if 'content' in request.POST and request.POST['content'].strip():
            post = Post(content=request.POST['content'], author=request.user)
            post.save()

            # Prepare data for JsonResponse
            data = {
                'id': post.id,
                'content': post.content,
                'author': post.author.username,
                'created_at': post.created_at.strftime("%B %d, %Y, %I:%M %p"),  # Format the timestamp
                'likes': post.likes,
                'user_liked': False
            }
            #return JsonResponse(data)
            return redirect('index')
        
        else:
            return JsonResponse({'error': "Content cannot be empty."}, status=400)
        
        
    

    
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    followers_count = user.followers.count()
    following_count = user.following.count()
    is_following = Follow.objects.filter(follower=request.user, following=user).exists() if request.user.is_authenticated else False

    if request.user.is_authenticated:
        for post in page_obj:
            post.user_liked = post.user_liked(request.user)

    return render(request, 'network/profile.html', {
        'profile_user': user,
        'page_obj': page_obj,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    })

@login_required
def toggle_follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow != request.user:
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if not created:
            follow.delete()
    return redirect('profile', username=username)

@login_required
def following(request):
    following_users = request.user.following.all().values_list('following', flat=True)
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    paginator = Paginator(posts, 10)


    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    for post in page_obj:
        post.user_liked = post.user_liked(request.user)

    return render(request, 'network/following.html', {'page_obj': page_obj})

@csrf_protect
@require_http_methods(["PUT"])
def edit_post(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to edit a post.'}, status=401)

    post = get_object_or_404(Post, pk=post_id, author=request.user)

    if post.author_id != request.user.id:
        return JsonResponse({'error': 'You do not have permission to edit this post.'}, status=403)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)

    content = data.get('content', '')

    if content:
        post.content = content
        post.save()
        return JsonResponse({'success': 'Post updated successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Content cannot be empty.'}, status=400)
      
@login_required
@require_POST
@csrf_exempt
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        post.likes = max(post.likes - 1, 0)
        liked = False
    else:
        post.likes += 1
        liked = True

    post.save()
    return JsonResponse({'likes': post.likes, 'liked': liked})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user_liked = post.user_liked(request.user)
    return render(request, 'post_detail.html', {'post': post, 'user_liked': user_liked})

def delete_post(request, post_id):
    if request.method == 'DELETE':
        post = get_object_or_404(Post, pk=post_id)
        if post.author == request.user:
            post.delete()
            return JsonResponse({'message': 'Post deleted successfully.'})
        else:
            return JsonResponse({'error': 'You are not authorized to delete this post.'}, status=403)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
        