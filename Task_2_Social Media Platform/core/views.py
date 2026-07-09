"""
Views for the Social Media Platform.

Each function handles one page or action:
- home            : Main feed showing all posts
- register        : User sign-up
- login_view      : User sign-in
- logout_view     : User sign-out
- profile         : View a user's profile
- edit_profile    : Edit your own profile
- create_post     : Create a new post
- post_detail     : View a single post and its comments
- edit_post       : Edit your own post
- delete_post     : Delete your own post
- like_post       : Like or unlike a post (AJAX)
- add_comment     : Add a comment to a post
- delete_comment  : Delete your own comment
- follow_user     : Follow or unfollow a user (AJAX)
- search_users    : Search users by username
- followers_list  : See who follows a user
- following_list  : See who a user follows
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import UserProfile, Post, Comment, Like, Follow
from .forms import RegisterForm, ProfileEditForm, PostForm, CommentForm


# ─────────────────────────────────────────────────────────
# Home Feed
# ─────────────────────────────────────────────────────────

def home(request):
    """
    Show all posts in chronological order (newest first).
    If the user is logged in, show if they liked each post.
    """
    posts = Post.objects.all().select_related('author', 'author__profile')
    comment_form = CommentForm()

    # Build a set of post IDs the current user has liked
    liked_post_ids = set()
    if request.user.is_authenticated:
        liked_post_ids = set(
            Like.objects.filter(user=request.user).values_list('post_id', flat=True)
        )

    return render(request, 'core/home.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids,
        'comment_form': comment_form,
    })


# ─────────────────────────────────────────────────────────
# Authentication
# ─────────────────────────────────────────────────────────

def register(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log them in right after signing up
            messages.success(request, f'Welcome to ConnectHub, {user.username}!')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            # Go to the page they were trying to visit, or home
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'core/login.html')


@login_required
def logout_view(request):
    """Log the user out and redirect to login page."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─────────────────────────────────────────────────────────
# User Profile
# ─────────────────────────────────────────────────────────

def profile(request, username):
    """
    Show a user's profile page.
    Displays their info, posts, followers, and following counts.
    """
    user = get_object_or_404(User, username=username)
    # Make sure the profile exists (create if missing)
    profile_obj, _ = UserProfile.objects.get_or_create(user=user)
    posts = Post.objects.filter(author=user).order_by('-created_at')

    # Check if the logged-in user is following this profile
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(
            follower=request.user, following=user
        ).exists()

    return render(request, 'core/profile.html', {
        'profile_user': user,
        'profile_obj': profile_obj,
        'posts': posts,
        'is_following': is_following,
        'followers_count': profile_obj.get_followers_count(),
        'following_count': profile_obj.get_following_count(),
        'posts_count': profile_obj.get_posts_count(),
    })


@login_required
def edit_profile(request):
    """Let the logged-in user edit their own profile."""
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=profile_obj)

    return render(request, 'core/edit_profile.html', {'form': form})


# ─────────────────────────────────────────────────────────
# Posts
# ─────────────────────────────────────────────────────────

@login_required
def create_post(request):
    """Let a logged-in user create a new post."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author to the logged-in user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'core/create_post.html', {'form': form})


def post_detail(request, post_id):
    """Show a single post with all its comments."""
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).select_related('author', 'author__profile')
    comment_form = CommentForm()

    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()

    return render(request, 'core/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
        'likes_count': post.get_likes_count(),
    })


@login_required
def edit_post(request, post_id):
    """Let the author edit their own post."""
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'core/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    """Let the author delete their own post."""
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('home')

    return render(request, 'core/delete_post.html', {'post': post})


# ─────────────────────────────────────────────────────────
# Likes (AJAX-friendly)
# ─────────────────────────────────────────────────────────

@login_required
@require_POST
def like_post(request, post_id):
    """
    Toggle like on a post.
    Returns JSON so JavaScript can update the page without reloading.
    """
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        # User already liked it – remove the like (unlike)
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': post.get_likes_count(),
    })


# ─────────────────────────────────────────────────────────
# Comments
# ─────────────────────────────────────────────────────────

@login_required
@require_POST
def add_comment(request, post_id):
    """Add a comment to a post."""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post   = post
        comment.author = request.user
        comment.save()
        messages.success(request, 'Comment added.')
    else:
        messages.error(request, 'Comment cannot be empty.')

    return redirect('post_detail', post_id=post_id)


@login_required
def delete_comment(request, comment_id):
    """Let a user delete their own comment."""
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    post_id = comment.post.id
    comment.delete()
    messages.success(request, 'Comment deleted.')
    return redirect('post_detail', post_id=post_id)


# ─────────────────────────────────────────────────────────
# Follow System (AJAX-friendly)
# ─────────────────────────────────────────────────────────

@login_required
@require_POST
def follow_user(request, username):
    """
    Toggle follow on a user.
    Returns JSON so JavaScript can update the button without reloading.
    """
    user_to_follow = get_object_or_404(User, username=username)

    # You can't follow yourself
    if request.user == user_to_follow:
        return JsonResponse({'error': 'You cannot follow yourself.'}, status=400)

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )

    if not created:
        # Already following – unfollow
        follow.delete()
        following = False
    else:
        following = True

    return JsonResponse({
        'following': following,
        'followers_count': Follow.objects.filter(following=user_to_follow).count(),
    })


# ─────────────────────────────────────────────────────────
# Search
# ─────────────────────────────────────────────────────────

def search_users(request):
    """Search users by username (case-insensitive)."""
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        results = User.objects.filter(
            username__icontains=query
        ).select_related('profile').exclude(id=request.user.id if request.user.is_authenticated else None)

    return render(request, 'core/search.html', {
        'results': results,
        'query': query,
    })


# ─────────────────────────────────────────────────────────
# Followers / Following Lists
# ─────────────────────────────────────────────────────────

def followers_list(request, username):
    """Show all users who follow this user."""
    user = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(following=user).select_related('follower', 'follower__profile')
    return render(request, 'core/followers_list.html', {
        'profile_user': user,
        'followers': followers,
    })


def following_list(request, username):
    """Show all users this user is following."""
    user = get_object_or_404(User, username=username)
    following = Follow.objects.filter(follower=user).select_related('following', 'following__profile')
    return render(request, 'core/following_list.html', {
        'profile_user': user,
        'following': following,
    })
