from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    # API
    path("api/dishes/batch/", batch_next_dishes, name="batch-next-dishes"),
    path("api/choices/", save_choice, name="save-choice"),
    path("api/favorites/", favorites_list, name="favorites-list"),
]
