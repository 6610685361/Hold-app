import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Food
from django.http import JsonResponse

def random_food(request):
    count = Food.objects.count()
    if count == 0:
        return JsonResponse({"error": "No food in database"})
    random_index = random.randint(0, count - 1)
    food = Food.objects.all()[random_index]
    return JsonResponse({
    "id": food.foodID,  # ← fixed here
    "name": food.name,
    "imageURL": food.imageURL,
    "description": food.description
    })


def random_food_page(request):
    foods = list(Food.objects.all())
    if not foods:
        return render(request, "RandomFood/Random.html", {"food": None})
    food = random.choice(foods)
    return render(request, "RandomFood/Random.html", {"food": food})

def you_chose_this(request, food_id):
    food = get_object_or_404(Food, foodID=food_id)
    return render(request, "RandomFood/YouChoseThis.html", {"food": food})

@login_required
def add_favorite(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    request.user.profile.favorites.add(food)
    return redirect("profile")


