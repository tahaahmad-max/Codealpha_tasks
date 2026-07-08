"""
populate_data.py — Sample product data loader

Run this script to add sample products to the database:
    python manage.py shell < populate_data.py
"""

from store.models import Product

# Clear existing products (optional — comment out to keep existing)
# Product.objects.all().delete()

sample_products = [
    {
        "name": "Wireless Noise-Cancelling Headphones",
        "description": "Experience premium sound quality with our flagship wireless headphones. Featuring active noise cancellation, 30-hour battery life, and ultra-comfortable ear cushions. Perfect for music lovers, travelers, and remote workers who demand the best audio experience.",
        "short_description": "Premium wireless headphones with 30hr battery & noise cancellation.",
        "price": 89.99,
        "stock": 25,
        "image": "products/headphones.jpg",
    },
    {
        "name": "Mechanical Gaming Keyboard",
        "description": "Level up your gaming setup with this tactile mechanical keyboard. Features RGB backlighting with 16 million colors, Cherry MX Blue switches, and a durable aluminum frame. Anti-ghosting technology ensures every keypress is registered.",
        "short_description": "RGB mechanical keyboard with Cherry MX switches and aluminum frame.",
        "price": 59.99,
        "stock": 40,
        "image": "products/mechanical-keyboard.jpg",
    },
    {
        "name": "4K Webcam Pro",
        "description": "Look your best in video calls with this 4K Ultra HD webcam. Includes a built-in ring light, wide-angle lens, automatic low-light correction, and a built-in noise-cancelling microphone. Plug-and-play — no drivers needed.",
        "short_description": "4K webcam with ring light, auto low-light, and built-in mic.",
        "price": 74.99,
        "stock": 18,
        "image": "products/webcam.jpg",
    },
    {
        "name": "Ergonomic Office Chair",
        "description": "Work comfortably for hours with this ergonomic office chair. Adjustable lumbar support, breathable mesh back, 360° swivel, and height adjustment. Designed by posture specialists to reduce back pain and boost productivity.",
        "short_description": "Ergonomic mesh chair with lumbar support and full adjustability.",
        "price": 249.99,
        "stock": 10,
        "image": "products/office-chair.jpg",
    },
    {
        "name": "Smart LED Desk Lamp",
        "description": "Illuminate your workspace with this smart LED desk lamp. Offers 5 color temperatures, 10 brightness levels, a built-in wireless phone charger, and a USB charging port. Touch controls and memory function included.",
        "short_description": "Smart LED lamp with wireless charger and 10 brightness levels.",
        "price": 39.99,
        "stock": 50,
        "image": "products/desk-lamp.jpg",
    },
    {
        "name": "Portable Bluetooth Speaker",
        "description": "Take your music anywhere with this rugged Bluetooth speaker. IPX7 waterproof rating, 360° surround sound, 12-hour playtime, and a built-in power bank to charge your phone. Connects to two devices simultaneously.",
        "short_description": "Waterproof Bluetooth speaker with 12hr battery and 360° sound.",
        "price": 49.99,
        "stock": 35,
        "image": "products/bluetooth-speaker.jpg",
    },
    {
        "name": "USB-C Hub (7-in-1)",
        "description": "Expand your laptop's connectivity with this versatile 7-in-1 USB-C hub. Includes 4K HDMI, 100W PD charging, 2× USB-A 3.0, SD & microSD card readers, and a USB-C data port. Compact and bus-powered — no external power needed.",
        "short_description": "7-in-1 USB-C hub with 4K HDMI, PD charging, and card readers.",
        "price": 34.99,
        "stock": 60,
        "image": "products/usb-c-hub.jpg",
    },
    {
        "name": "Laptop Stand (Adjustable)",
        "description": "Improve your posture with this premium aluminum laptop stand. Adjustable to 6 heights and 2 angles, folds flat for easy transport, and works with laptops from 11\" to 17\". Heat-dissipating design keeps your laptop cool.",
        "short_description": "Aluminum adjustable laptop stand, foldable, fits 11\"–17\" laptops.",
        "price": 29.99,
        "stock": 45,
        "image": "products/laptop-stand.jpg",
    },
]

created = 0
for data in sample_products:
    product, was_created = Product.objects.get_or_create(
        name=data["name"],
        defaults=data
    )
    if was_created:
        created += 1
        print(f"  ✅ Created: {product.name}")
    else:
        print(f"  ⚠️  Already exists: {product.name}")

print(f"\nDone! {created} new products added.")
