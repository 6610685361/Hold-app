from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Dish, Choice
import random, json

def home(request):
    dishes = list(Dish.objects.all())
    random.shuffle(dishes)
    cards = dishes[:3]  # เอาแค่ 3 ใบ
    return render(request, "pages/home.html", {"cards": cards})

def about(request):
    return render(request, "pages/AboutUs.html")

@login_required
def batch_next_dishes(request):
    """ส่งการ์ดแบบสุ่ม n ใบ (default 3) โดยตัดเมนูที่ผู้ใช้ตัดสินใจไปแล้ว"""
    n = int(request.GET.get("n", 3))
    decided = Choice.objects.filter(user=request.user).values_list('dish_id', flat=True)
    qs = Dish.objects.exclude(id__in=decided)

    if not qs.exists():
        return JsonResponse({"cards": [], "done": True})

    base_ids = list(qs.values_list('id', flat=True)[:200])  # limit เพื่อเบา DB
    pick_ids = random.sample(base_ids, k=min(n, len(base_ids)))
    dishes = Dish.objects.filter(id__in=pick_ids)

    cards = [{
        "id": d.id,
        "name": d.name,
        "cuisine": d.cuisine,
        "image_url": d.image_url,
    } for d in dishes]

    return JsonResponse({"cards": cards, "done": len(cards) < n})

@login_required
@require_http_methods(["POST"])
def save_choice(request):
    """รับผลการปัด: {"dish_id": 1, "action": "LIKE"|"SKIP"}"""
    payload = json.loads(request.body or "{}")
    dish_id = payload.get("dish_id")
    action = payload.get("action")
    if action not in ("LIKE", "SKIP") or not dish_id:
        return JsonResponse({"error": "bad payload"}, status=400)

    Choice.objects.update_or_create(
        user=request.user, dish_id=dish_id,
        defaults={"action": action}
    )
    return JsonResponse({"ok": True})

@login_required
def favorites_list(request):
    likes = (Choice.objects
             .filter(user=request.user, action=Choice.LIKE)
             .select_related("dish")
             .order_by("-created_at")[:30])
    data = [{
        "id": c.dish.id,
        "name": c.dish.name,
        "cuisine": c.dish.cuisine,
        "image_url": c.dish.image_url,
    } for c in likes]
    return JsonResponse({"favorites": data})
