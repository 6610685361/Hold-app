import random
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Food
from accounts.models import UserProfile

# === Regular HTML pages ===


def random_food_page(request):
    """Main page that loads the interactive swipe UI"""
    return render(request, "RandomFood/home.html")


# def you_chose_this(request, food_id):
#     food = get_object_or_404(Food, pk=food_id)
#     return render(request, "RandomFood/youchosethis.html", {"food": food})


@login_required
def add_favorite(request, food_id):
    """(optional simple version kept)"""
    food = get_object_or_404(Food, pk=food_id)
    request.user.profile.favorites.add(food)
    return redirect("profile")


# === API endpoints for frontend ===


def api_random_food_batch(request):
    """Return random n foods starting from offset as JSON"""
    n = request.GET.get("n")
    offset = request.GET.get("offset", 0)
    try:
        n = int(n) if n else 3
        offset = int(offset)
    except:
        n = 3
        offset = 0

    foods = list(Food.objects.all())
    if not foods:
        return JsonResponse({"cards": [], "done": True})

    random.shuffle(foods)
    cards = foods[offset : offset + n]

    data = [
        {
            "id": f.pk,
            "name": f.name,
            "description": f.description or "",
            "image_url": f.imageURL or "",
        }
        for f in cards
    ]
    done = (offset + n) >= len(foods)
    return JsonResponse({"cards": data, "done": done})


def api_add_favorite(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        payload = json.loads(request.body or "{}")
        food_id = payload.get("dish_id") or payload.get("food_id")
        if not food_id:
            return JsonResponse({"error": "No dish_id provided"}, status=400)

        food = get_object_or_404(Food, pk=food_id)

        # get or create profile
        profile, _ = UserProfile.objects.get_or_create(user=request.user)

        # add favorite if not already
        profile.favorites.add(food)

        return JsonResponse({"ok": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
def api_get_favorites(request):
    """Return list of current user's favorite foods."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    favs = profile.favorites.all()
    data = [
        {
            "id": f.pk,
            "name": f.name,
            "image_url": f.imageURL or "",
        }
        for f in favs
    ]
    return JsonResponse({"favorites": data})
