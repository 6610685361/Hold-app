from django.shortcuts import render
import random
from django.http import JsonResponse
from .models import Food

def random_food(request):
    count = Food.objects.count()
    if count == 0:
        return JsonResponse({"error": "No food in database"})
    random_index = random.randint(0, count - 1)
    food = Food.objects.all()[random_index]
    return JsonResponse({
        "foodID": food.foodID,
        "name": food.name,
        "imageURL": food.imageURL,
        "description": food.description
    })

def random_food_page(request):
    return render(request, "RandomFood/Random.html")

