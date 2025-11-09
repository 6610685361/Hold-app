from django.urls import path
from . import views

urlpatterns = [
    path('', views.random_food_page, name='random_food_page'),
    path("api/random-food/", views.random_food, name="random_food"),
]
