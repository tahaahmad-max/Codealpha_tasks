# ConnectHub – Social Media Platform

A beginner-friendly social media web application built with **Django** and **Vanilla JavaScript**.

---

## Features

- **Home Feed** – All posts in chronological order with likes and comments
- **User Auth** – Register, Login, Logout with Django's built-in system
- **User Profiles** – Avatar, bio, follower/following counts, posts grid
- **Create Posts** – Text captions + optional image upload
- **Edit / Delete Posts** – Author-only controls
- **Comments** – Add and delete comments on any post
- **Like System** – Like/unlike with real-time AJAX updates
- **Follow System** – Follow/unfollow users with AJAX
- **Search Users** – Search by username
- **Admin Panel** – Full Django admin at `/admin/`

---

## Project Structure

```
Social Media Platform/
├── core/                   # Main Django app
│   ├── migrations/
│   ├── admin.py            # Admin panel setup
│   ├── forms.py            # All forms
│   ├── models.py           # Database models
│   ├── urls.py             # App URL routes
│   └── views.py            # View functions
├── socialmedia/            # Django project config
│   ├── settings.py
│   └── urls.py
├── templates/
│   └── core/               # All HTML templates
│       ├── base.html
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       ├── edit_profile.html
│       ├── create_post.html
│       ├── edit_post.html
│       ├── delete_post.html
│       ├── post_detail.html
│       ├── search.html
│       ├── followers_list.html
│       └── following_list.html
├── static/
│   ├── css/style.css       # Main stylesheet
│   └── js/main.js          # JavaScript (AJAX likes/follows)
├── media/                  # User-uploaded images (auto-created)
├── populate_data.py        # Script to add sample data
├── requirements.txt
└── manage.py
```

---

## Database Models

| Model       | Description                              |
|-------------|------------------------------------------|
| UserProfile | Extends User with bio + profile picture  |
| Post        | Caption + optional image + author + date |
| Comment     | Text comment linked to a post            |
| Like        | User ↔ Post (unique per pair)            |
| Follow      | Follower ↔ Following (unique per pair)   |

---

## Installation & Setup

### 1. Clone / download the project

```
cd "Social Media Platform"
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run database migrations

```bash
python manage.py makemigrations core
python manage.py migrate
```

### 4. Create a superuser (for admin panel)

```bash
python manage.py createsuperuser
```
> Or use the pre-created admin: **username:** `admin` | **password:** `Admin1234!`

### 5. Add sample data (optional)

```bash
python populate_data.py
```

### 6. Start the development server

```bash
python manage.py runserver
```

### 7. Open in browser

```
http://127.0.0.1:8000
```

Admin panel: `http://127.0.0.1:8000/admin/`

---

## Test Accounts (after running populate_data.py)

| Username | Password   |
|----------|------------|
| alice    | Test1234!  |
| bob      | Test1234!  |
| charlie  | Test1234!  |
| admin    | Admin1234! |

---

## Tech Stack

- **Backend:** Python 3.x + Django 4.2
- **Database:** SQLite (built-in, no setup needed)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Images:** Pillow (for image processing)
- **Fonts:** Google Fonts (Inter)
