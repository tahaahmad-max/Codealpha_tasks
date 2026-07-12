# ProjectFlow - Project Management Tool

A beginner-friendly project management tool similar to Trello/Asana, built with Django and vanilla HTML/CSS/JS.

## Features
- User registration, login, logout
- Project creation with member management
- Kanban board (To Do / In Progress / Completed)
- Task management with priority, due dates, assignments
- Comments on tasks
- Notifications system
- User profiles with avatars
- Full Django Admin panel

## Quick Start

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Apply migrations
```
python manage.py makemigrations
python manage.py migrate
```

### 3. Populate sample data
```
python populate_db.py
```

### 4. Run the server
```
python manage.py runserver
```

Open: **http://127.0.0.1:8000/**

## Login Credentials

| Username | Password    | Role       |
|----------|-------------|------------|
| admin    | Admin@1234  | Superuser  |
| alice    | Alice@1234  | User       |
| bob      | Bob@12345   | User       |
| carol    | Carol@1234  | User       |

## Admin Panel
Visit: **http://127.0.0.1:8000/admin/**  
Login with: `admin / Admin@1234`

## Create Superuser (manually)
```
python manage.py createsuperuser
```

## Project Structure
```
Project Management Tool/
├── accounts/        # Auth, user profiles
├── projects/        # Projects, members
├── tasks/           # Tasks, comments, notifications
├── templates/       # HTML templates
├── static/          # CSS & JS
├── media/           # Uploaded files
├── populate_db.py   # Sample data
└── requirements.txt
```
