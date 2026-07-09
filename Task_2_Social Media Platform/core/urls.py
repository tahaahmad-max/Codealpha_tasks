"""
URL patterns for the core app.
Maps each URL path to its view function.
"""

from django.urls import path
from . import views

urlpatterns = [
    # ── Home ──────────────────────────────────────────────
    path('', views.home, name='home'),

    # ── Authentication ────────────────────────────────────
    path('register/', views.register,       name='register'),
    path('login/',    views.login_view,     name='login'),
    path('logout/',   views.logout_view,    name='logout'),

    # ── Profile ───────────────────────────────────────────
    path('profile/<str:username>/', views.profile,      name='profile'),
    path('profile/edit/me/',        views.edit_profile, name='edit_profile'),

    # ── Posts ─────────────────────────────────────────────
    path('post/create/',             views.create_post,  name='create_post'),
    path('post/<int:post_id>/',      views.post_detail,  name='post_detail'),
    path('post/<int:post_id>/edit/', views.edit_post,    name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),

    # ── Likes ─────────────────────────────────────────────
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),

    # ── Comments ──────────────────────────────────────────
    path('post/<int:post_id>/comment/',       views.add_comment,    name='add_comment'),
    path('comment/<int:comment_id>/delete/',  views.delete_comment, name='delete_comment'),

    # ── Follow ────────────────────────────────────────────
    path('follow/<str:username>/',              views.follow_user,    name='follow_user'),
    path('followers/<str:username>/',           views.followers_list, name='followers_list'),
    path('following/<str:username>/',           views.following_list, name='following_list'),

    # ── Search ────────────────────────────────────────────
    path('search/', views.search_users, name='search'),
]
