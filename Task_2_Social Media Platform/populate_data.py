"""
populate_data.py – Creates sample users, profiles, posts, comments, likes, and follows.
Run with:  python manage.py shell < populate_data.py
Or:        python populate_data.py  (from project root with manage.py in PATH)
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialmedia.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, Post, Comment, Like, Follow

print("Creating sample data...")

# ── Users ──
users_data = [
    {'username': 'alice',   'first_name': 'Alice',  'last_name': 'Smith',   'email': 'alice@example.com',   'password': 'Test1234!'},
    {'username': 'bob',     'first_name': 'Bob',    'last_name': 'Johnson', 'email': 'bob@example.com',     'password': 'Test1234!'},
    {'username': 'charlie', 'first_name': 'Charlie','last_name': 'Brown',   'email': 'charlie@example.com', 'password': 'Test1234!'},
]

created_users = []
for u in users_data:
    user, created = User.objects.get_or_create(username=u['username'])
    if created:
        user.set_password(u['password'])
        user.first_name = u['first_name']
        user.last_name  = u['last_name']
        user.email      = u['email']
        user.save()
        print(f"  Created user: {user.username}")
    else:
        print(f"  User already exists: {user.username}")
    profile, _ = UserProfile.objects.get_or_create(user=user)
    if created:
        bios = {
            'alice':   'Photography enthusiast & coffee lover ☕',
            'bob':     'Software developer by day, gamer by night 🎮',
            'charlie': 'Traveler | Foodie | Life is short, eat dessert first 🍰',
        }
        profile.bio = bios.get(user.username, '')
        profile.save()
    created_users.append(user)

alice, bob, charlie = created_users

# ── Posts ──
posts_data = [
    {'author': alice,   'caption': 'Just had the most amazing sunrise hike this morning! 🌅 Nature never fails to amaze me. #hiking #nature #sunrise'},
    {'author': bob,     'caption': 'Finally finished my personal project after 3 months of work. Feels so good to ship something! 🚀 #coding #developer #shipping'},
    {'author': charlie, 'caption': 'Tried making homemade pasta for the first time. It was... an adventure. 🍝 But totally worth it! #cooking #food #homemade'},
    {'author': alice,   'caption': 'Reading a great book this weekend. There is nothing better than a good story and a warm cup of tea. 📚 #reading #books'},
    {'author': bob,     'caption': 'Pro tip: Take breaks. Your future self will thank you. Step away from the screen for a while every day! 💡 #productivity'},
]

created_posts = []
for p in posts_data:
    post = Post.objects.create(author=p['author'], caption=p['caption'])
    created_posts.append(post)
    print(f"  Created post #{post.id} by {post.author.username}")

# ── Comments ──
Comment.objects.get_or_create(post=created_posts[0], author=bob,     defaults={'text': 'Wow, that sounds incredible! 😍'})
Comment.objects.get_or_create(post=created_posts[0], author=charlie, defaults={'text': 'I need to do this too!'})
Comment.objects.get_or_create(post=created_posts[1], author=alice,   defaults={'text': 'Congratulations! 🎉 That must feel amazing!'})
Comment.objects.get_or_create(post=created_posts[2], author=bob,     defaults={'text': 'Homemade pasta is the best kind of pasta 🍝'})
Comment.objects.get_or_create(post=created_posts[3], author=charlie, defaults={'text': 'What book are you reading?'})
print("  Created sample comments")

# ── Likes ──
for post in created_posts[:3]:
    Like.objects.get_or_create(post=post, user=bob)
    Like.objects.get_or_create(post=post, user=charlie)
Like.objects.get_or_create(post=created_posts[0], user=bob)
print("  Created sample likes")

# ── Follows ──
Follow.objects.get_or_create(follower=bob,     following=alice)
Follow.objects.get_or_create(follower=charlie, following=alice)
Follow.objects.get_or_create(follower=alice,   following=bob)
Follow.objects.get_or_create(follower=charlie, following=bob)
print("  Created sample follows")

print("\n✅ Sample data created successfully!")
print("\nTest Accounts:")
print("  username: alice   | password: Test1234!")
print("  username: bob     | password: Test1234!")
print("  username: charlie | password: Test1234!")
