import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Food


def random_food_page(request):
    # better: avoid loading all objects into memory if many records
    food = Food.objects.order_by("?").first()
    if not food:
        return render(request, "RandomFood/random.html", {"food": None})
    return render(request, "RandomFood/random.html", {"food": food})


def you_chose_this(request, food_id):
    food = get_object_or_404(Food, pk=food_id)
    return render(request, "RandomFood/youchosethis.html", {"food": food})


@login_required
def add_favorite(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    request.user.profile.favorites.add(food)
    return redirect("profile")
