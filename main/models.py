from django.conf import settings
from django.db import models

class Dish(models.Model):
    name = models.CharField(max_length=200)
    cuisine = models.CharField(max_length=50, blank=True)
    image_url = models.URLField(blank=True)

    main_ingredients = models.TextField(blank=True)
    energy_kcal = models.IntegerField(null=True, blank=True)
    protein_g = models.IntegerField(null=True, blank=True)
    carbs_g = models.IntegerField(null=True, blank=True)
    fat_g = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Choice(models.Model):
    LIKE = 'LIKE'
    SKIP = 'SKIP'
    ACTIONS = [(LIKE, 'Like'), (SKIP, 'Skip')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dish  = models.ForeignKey(Dish, on_delete=models.CASCADE)
    action = models.CharField(max_length=4, choices=ACTIONS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'dish')
