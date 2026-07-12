"""
populate_db.py - Seeds the database with sample users, projects, and tasks.
Run with: python populate_db.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectmanager.settings')
django.setup()

from django.contrib.auth.models import User
from projects.models import Project, ProjectMember
from tasks.models import Task, Comment
from datetime import date, timedelta

print("Seeding database...")

# --- Create Users ---
users_data = [
    {'username': 'admin', 'email': 'admin@example.com', 'password': 'Admin@1234', 'first_name': 'Admin', 'last_name': 'User', 'is_staff': True, 'is_superuser': True},
    {'username': 'alice', 'email': 'alice@example.com', 'password': 'Alice@1234', 'first_name': 'Alice', 'last_name': 'Johnson'},
    {'username': 'bob', 'email': 'bob@example.com', 'password': 'Bob@12345', 'first_name': 'Bob', 'last_name': 'Smith'},
    {'username': 'carol', 'email': 'carol@example.com', 'password': 'Carol@1234', 'first_name': 'Carol', 'last_name': 'Williams'},
]

created_users = {}
for u in users_data:
    if not User.objects.filter(username=u['username']).exists():
        user = User.objects.create_user(
            username=u['username'], email=u['email'], password=u['password'],
            first_name=u['first_name'], last_name=u['last_name'],
        )
        user.is_staff = u.get('is_staff', False)
        user.is_superuser = u.get('is_superuser', False)
        user.save()
        print(f"  Created user: {u['username']}")
    else:
        user = User.objects.get(username=u['username'])
        print(f"  User already exists: {u['username']}")
    created_users[u['username']] = user

alice = created_users['alice']
bob = created_users['bob']
carol = created_users['carol']

# --- Create Projects ---
if not Project.objects.filter(name='Website Redesign').exists():
    p1 = Project.objects.create(
        name='Website Redesign',
        description='Complete overhaul of the company website with modern design.',
        owner=alice
    )
    ProjectMember.objects.create(project=p1, user=bob, role='admin')
    ProjectMember.objects.create(project=p1, user=carol, role='member')

    tasks_p1 = [
        {'title': 'Design wireframes', 'desc': 'Create wireframes for all main pages.', 'priority': 'high', 'status': 'done', 'assigned': alice, 'days': -5},
        {'title': 'Build homepage', 'desc': 'Implement the new homepage layout.', 'priority': 'high', 'status': 'inprogress', 'assigned': bob, 'days': 3},
        {'title': 'Write content', 'desc': 'Draft all page content and copy.', 'priority': 'medium', 'status': 'todo', 'assigned': carol, 'days': 7},
        {'title': 'SEO optimization', 'desc': 'Optimize all pages for search engines.', 'priority': 'low', 'status': 'todo', 'assigned': None, 'days': 14},
    ]
    for t in tasks_p1:
        task = Task.objects.create(
            project=p1, title=t['title'], description=t['desc'],
            priority=t['priority'], status=t['status'],
            assigned_to=t['assigned'], created_by=alice,
            due_date=date.today() + timedelta(days=t['days'])
        )
    Comment.objects.create(task=Task.objects.filter(project=p1).first(), author=bob, body='Great work on the wireframes, Alice!')
    print("  Created project: Website Redesign")

if not Project.objects.filter(name='Mobile App Development').exists():
    p2 = Project.objects.create(
        name='Mobile App Development',
        description='Build a cross-platform mobile app for iOS and Android.',
        owner=bob
    )
    ProjectMember.objects.create(project=p2, user=alice, role='member')

    tasks_p2 = [
        {'title': 'Setup project structure', 'desc': 'Initialize the React Native project.', 'priority': 'high', 'status': 'done', 'assigned': bob, 'days': -3},
        {'title': 'User authentication flow', 'desc': 'Implement login and register screens.', 'priority': 'high', 'status': 'inprogress', 'assigned': bob, 'days': 5},
        {'title': 'Dashboard screen', 'desc': 'Build the main dashboard UI.', 'priority': 'medium', 'status': 'todo', 'assigned': alice, 'days': 10},
    ]
    for t in tasks_p2:
        Task.objects.create(
            project=p2, title=t['title'], description=t['desc'],
            priority=t['priority'], status=t['status'],
            assigned_to=t['assigned'], created_by=bob,
            due_date=date.today() + timedelta(days=t['days'])
        )
    print("  Created project: Mobile App Development")

print("\nDone! Sample data created.")
print("\nLogin credentials:")
print("  admin / Admin@1234  (superuser)")
print("  alice / Alice@1234")
print("  bob   / Bob@12345")
print("  carol / Carol@1234")
print("\nRun: python manage.py runserver")
