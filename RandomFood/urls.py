from django.urls import path
from . import views

urlpatterns = [
    path("", views.random_food_page, name="random_food_page"),
    path("you-chose/<int:food_id>/", views.you_chose_this, name="you_chose_this"),
    path("add-favorite/<int:food_id>/", views.add_favorite, name="add_favorite"),
]

