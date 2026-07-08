# ShopEase — Simple E-Commerce Store

A beginner-friendly Django e-commerce project built with HTML, CSS, and Vanilla JavaScript.

---

## Quick Start

### Step 1 — Install Python & Django

Make sure Python 3.10+ is installed. Then install dependencies:

```bash
pip install -r requirements.txt
```

### Step 2 — Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3 — Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

Enter a username, email, and password when prompted.

### Step 4 — Add Sample Products

```bash
python manage.py shell < populate_data.py
```

### Step 5 — Run the Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

Admin panel: **http://127.0.0.1:8000/admin/**

---

## Project Structure

```
Simple E-Commerce Store/
│
├── manage.py                   # Django CLI entry point
├── requirements.txt            # Python dependencies
├── populate_data.py            # Sample product loader
├── db.sqlite3                  # SQLite database (auto-created)
│
├── ecommerce/                  # Django project config
│   ├── settings.py             # All settings
│   ├── urls.py                 # Root URL routing
│   └── wsgi.py
│
├── store/                      # Main app
│   ├── models.py               # Product, Order, OrderItem
│   ├── views.py                # Page logic (products, cart, orders)
│   ├── auth_views.py           # Login, register, logout
│   ├── urls.py                 # Store URL routes
│   ├── auth_urls.py            # Auth URL routes
│   ├── forms.py                # RegisterForm, CheckoutForm
│   ├── admin.py                # Django Admin config
│   ├── cart.py                 # Session-based shopping cart
│   ├── context_processors.py   # Cart count for navbar
│   └── apps.py
│
├── templates/                  # HTML templates
│   ├── base.html               # Shared layout (navbar, footer)
│   ├── store/
│   │   ├── home.html           # Product listing grid
│   │   ├── product_detail.html # Single product page
│   │   ├── cart.html           # Shopping cart
│   │   ├── checkout.html       # Checkout form
│   │   ├── order_confirmation.html
│   │   ├── order_list.html     # My Orders page
│   │   └── order_detail.html   # Single order page
│   └── auth/
│       ├── login.html
│       └── register.html
│
├── static/
│   ├── css/style.css           # All styling
│   └── js/main.js              # Frontend JavaScript
│
└── media/                      # Uploaded product images (auto-created)
    └── products/
```

---

## Pages & URLs

| Page               | URL                          | Login Required |
|--------------------|------------------------------|----------------|
| Home / Products    | `/`                          | No             |
| Product Detail     | `/product/<id>/`             | No             |
| Shopping Cart      | `/cart/`                     | No             |
| Checkout           | `/checkout/`                 | ✅ Yes         |
| Order Confirmation | `/order/confirmation/<id>/`  | ✅ Yes         |
| My Orders          | `/orders/`                   | ✅ Yes         |
| Order Detail       | `/orders/<id>/`              | ✅ Yes         |
| Register           | `/auth/register/`            | No             |
| Login              | `/auth/login/`               | No             |
| Logout             | `/auth/logout/`              | No             |
| Admin Panel        | `/admin/`                    | Superuser only |

---

## Database Models

### Product
| Field             | Type        | Description                    |
|-------------------|-------------|--------------------------------|
| name              | CharField   | Product name                   |
| description       | TextField   | Full description               |
| short_description | CharField   | Brief summary for cards        |
| price             | Decimal     | Price (e.g., 29.99)            |
| image             | ImageField  | Optional product photo         |
| stock             | Integer     | Available units                |
| created_at        | DateTime    | Auto-set on creation           |

### Order
| Field      | Type      | Description                          |
|------------|-----------|--------------------------------------|
| user       | FK→User   | Who placed the order                 |
| status     | Choice    | pending / processing / shipped / delivered |
| full_name  | Char      | Shipping name                        |
| email      | Email     | Contact email                        |
| address    | Text      | Street address                       |
| city       | Char      | City                                 |
| zip_code   | Char      | ZIP/postal code                      |
| created_at | DateTime  | When order was placed                |

### OrderItem
| Field              | Type       | Description                  |
|--------------------|------------|------------------------------|
| order              | FK→Order   | Parent order                 |
| product            | FK→Product | The product purchased        |
| quantity           | Integer    | How many units               |
| price_at_purchase  | Decimal    | Price locked at time of sale |

---

## Admin Panel

Log in at `/admin/` with your superuser credentials.

**Products** — Add, edit, delete products. Edit price & stock directly from list view.

**Orders** — View all orders with status. Click an order to see items inline. Update status (Pending → Processing → Shipped → Delivered).

---

## Adding Product Images

1. Go to `/admin/` → Products → Add Product
2. Fill in name, description, price, stock
3. Click **"Choose File"** under Image to upload a photo
4. Save — the image appears on the home page and product detail page

---

## Common Commands

```bash
# Start development server
python manage.py runserver

# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Load sample products
python manage.py shell < populate_data.py

# Open Django interactive shell
python manage.py shell

# Collect static files (production only)
python manage.py collectstatic
```

---

## Tech Stack

| Layer     | Technology              |
|-----------|-------------------------|
| Backend   | Django 4.2 (Python)     |
| Database  | SQLite                  |
| Frontend  | HTML5, CSS3, Vanilla JS |
| Fonts     | Google Fonts (Inter)    |
| Images    | Pillow                  |

---

## Features

- ✅ Product grid with images, descriptions, prices
- ✅ Product detail page with quantity selector
- ✅ Session-based shopping cart (works without login)
- ✅ User registration & login
- ✅ Protected checkout (login required)
- ✅ Order saved to database with price snapshot
- ✅ Order confirmation page
- ✅ Order history for each user
- ✅ Django Admin for full product & order management
- ✅ Responsive design (mobile + desktop)
- ✅ Flash messages for user feedback
- ✅ Out-of-stock handling
