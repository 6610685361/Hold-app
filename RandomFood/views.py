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
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if food not in profile.favorites.all():
        profile.favorites.add(food)
        food.favorite_count = max(0, food.favorite_count - 1)
        food.save()
        action = "removed"
    else:
        profile.favorites.add(food)
        food.favorite_count += 1
        food.save()
        action = "added"

    return JsonResponse(
        {"ok": True, "action": action, "favorite_count": food.favorite_count}
    )


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

        if food in profile.favorites.all():
            profile.favorites.remove(food)
            food.favorite_count = max(0, food.favorite_count - 1)
            food.save()
            return JsonResponse(
                {"status": "removed", "favorite_count": food.favorite_count}
            )
        else:
            profile.favorites.add(food)
            food.favorite_count += 1
            food.save()
            return JsonResponse(
                {"status": "added", "favorite_count": food.favorite_count}
            )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
def remove_favorite(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if food in profile.favorites.all():
        profile.favorites.remove(food)
        # ลด favorite count
        if food.favorite_count > 0:
            food.favorite_count -= 1
            food.save()

    return JsonResponse({"ok": True, "removed": food_id})


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
