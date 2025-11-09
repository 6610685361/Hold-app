from django.urls import path
from . import views

urlpatterns = [
    path("", views.random_food_page, name="random_food_page"),
    path("api/foods/batch/", views.api_random_food_batch, name="api_random_food_batch"),
    path("api/favorites/add/", views.api_add_favorite, name="api_add_favorite"),
    path("api/favorites/", views.api_get_favorites, name="api_get_favorites"),
]
