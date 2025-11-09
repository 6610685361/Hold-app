# seed_data.py  — รันได้จากตำแหน่งไหนก็ได้ในโปรเจกต์
import os, sys
from pathlib import Path

here = Path(__file__).resolve()
root = here
# ไต่ขึ้นไปจนกว่าจะเจอ manage.py
while root != root.parent and not (root / "manage.py").exists():
    root = root.parent

if not (root / "manage.py").exists():
    raise SystemExit("manage.py not found. Run this file somewhere inside the Django project.")

sys.path.insert(0, str(root))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Hold.settings")

import django
django.setup()

from main.models import Dish

def pic(seed):
    return f"https://picsum.photos/seed/{seed.replace(' ', '').lower()}/800/600"

data = [
    dict(name="Pad Thai", cuisine="Thai", main_ingredients="Rice noodles, shrimp/chicken, tofu, egg, bean sprouts, tamarind sauce, peanuts", energy_kcal=425, protein_g=20, carbs_g=55, fat_g=12),
    dict(name="Green Curry (Kaeng Khiao Wan)", cuisine="Thai", main_ingredients="Coconut milk, green curry paste, chicken, Thai eggplant, basil", energy_kcal=500, protein_g=25, carbs_g=20, fat_g=35),
    dict(name="Tom Yum Goong", cuisine="Thai", main_ingredients="Shrimp, lemongrass, galangal, lime, chili paste, mushrooms", energy_kcal=200, protein_g=18, carbs_g=8, fat_g=10),
    dict(name="Som Tum (Papaya Salad)", cuisine="Thai", main_ingredients="Green papaya, tomato, chili, lime, peanuts, fish sauce", energy_kcal=150, protein_g=4, carbs_g=20, fat_g=6),
    dict(name="Massaman Curry", cuisine="Thai", main_ingredients="Beef, coconut milk, potato, onion, roasted peanuts, curry paste", energy_kcal=600, protein_g=30, carbs_g=25, fat_g=40),

    dict(name="Sushi (Mixed Nigiri)", cuisine="Japanese", main_ingredients="Vinegared rice, salmon, tuna, shrimp, nori, soy sauce", energy_kcal=300, protein_g=22, carbs_g=40, fat_g=6),
    dict(name="Ramen", cuisine="Japanese", main_ingredients="Wheat noodles, pork broth, egg, chashu, green onion, bamboo shoots", energy_kcal=550, protein_g=25, carbs_g=60, fat_g=20),
    dict(name="Tempura", cuisine="Japanese", main_ingredients="Shrimp or vegetables, flour batter, oil, dipping sauce", energy_kcal=400, protein_g=18, carbs_g=35, fat_g=22),
    dict(name="Tonkatsu", cuisine="Japanese", main_ingredients="Breaded deep-fried pork cutlet, cabbage, tonkatsu sauce", energy_kcal=550, protein_g=30, carbs_g=45, fat_g=28),
    dict(name="Okonomiyaki", cuisine="Japanese", main_ingredients="Cabbage, flour, egg, pork belly, bonito flakes, okonomi sauce", energy_kcal=450, protein_g=22, carbs_g=40, fat_g=20),

    dict(name="Spaghetti Bolognese", cuisine="Western", main_ingredients="Spaghetti, minced beef, tomato sauce, onion, garlic", energy_kcal=550, protein_g=30, carbs_g=65, fat_g=18),
    dict(name="Caesar Salad", cuisine="Western", main_ingredients="Romaine lettuce, croutons, Parmesan, Caesar dressing, chicken", energy_kcal=300, protein_g=25, carbs_g=15, fat_g=18),
    dict(name="Grilled Steak", cuisine="Western", main_ingredients="Beef steak, olive oil, salt, pepper, vegetables", energy_kcal=600, protein_g=50, carbs_g=5, fat_g=40),
    dict(name="Cheeseburger", cuisine="Western", main_ingredients="Beef patty, cheese, bun, lettuce, tomato, mayonnaise", energy_kcal=550, protein_g=30, carbs_g=40, fat_g=30),
    dict(name="Fish and Chips", cuisine="Western", main_ingredients="Cod, flour batter, potatoes, oil, tartar sauce", energy_kcal=700, protein_g=35, carbs_g=60, fat_g=35),

    dict(name="Pho (Beef Noodle Soup)", cuisine="Vietnamese", main_ingredients="Rice noodles, beef slices, onion, bean sprouts, herbs", energy_kcal=400, protein_g=25, carbs_g=45, fat_g=10),
    dict(name="Banh Mi", cuisine="Vietnamese", main_ingredients="Baguette, pork/chicken, pate, cucumber, carrot, cilantro", energy_kcal=500, protein_g=25, carbs_g=55, fat_g=20),
    dict(name="Goi Cuon (Fresh Spring Rolls)", cuisine="Vietnamese", main_ingredients="Rice paper, shrimp, vermicelli, lettuce, herbs", energy_kcal=180, protein_g=12, carbs_g=20, fat_g=5),
    dict(name="Bun Cha", cuisine="Vietnamese", main_ingredients="Grilled pork, vermicelli, fish sauce, herbs", energy_kcal=500, protein_g=30, carbs_g=45, fat_g=20),
    dict(name="Com Tam (Broken Rice with Pork)", cuisine="Vietnamese", main_ingredients="Broken rice, grilled pork chop, egg, pickled vegetables", energy_kcal=600, protein_g=35, carbs_g=50, fat_g=25),
]

for d in data:
    d.setdefault("image_url", pic(d["name"]))

# กันซ้ำตาม (name, cuisine)
from main.models import Dish
for d in data:
    Dish.objects.filter(name=d["name"], cuisine=d["cuisine"]).delete()

objs = [Dish(**d) for d in data]
Dish.objects.bulk_create(objs)
print(f"Seeded {len(objs)} dishes successfully.")
