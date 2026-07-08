"""
update_product_images.py — Assigns real product images to existing DB records.

Run via:
    python manage.py shell < update_product_images.py
"""

from store.models import Product

# Map exact product names to image filenames (relative to MEDIA_ROOT)
IMAGE_MAP = {
    "Wireless Noise-Cancelling Headphones": "products/headphones.jpg",
    "Mechanical Gaming Keyboard":           "products/mechanical-keyboard.jpg",
    "4K Webcam Pro":                        "products/webcam.jpg",
    "Ergonomic Office Chair":               "products/office-chair.jpg",
    "Smart LED Desk Lamp":                  "products/desk-lamp.jpg",
    "Portable Bluetooth Speaker":           "products/bluetooth-speaker.jpg",
    "USB-C Hub (7-in-1)":                   "products/usb-c-hub.jpg",
    "Laptop Stand (Adjustable)":            "products/laptop-stand.jpg",
}

updated = 0
not_found = []

for name, image_path in IMAGE_MAP.items():
    product = Product.objects.filter(name=name).first()
    if product:
        product.image = image_path
        product.save()
        updated += 1
        print(f"  ✅ Updated: {product.name!r} → {image_path}")
    else:
        not_found.append(name)
        print(f"  ⚠️  Not found in DB: {name!r}")

print(f"\n{'='*50}")
print(f"Done! {updated} products updated with images.")
if not_found:
    print(f"\n⚠️  Missing products (run populate_data.py first):")
    for n in not_found:
        print(f"   - {n}")
