from django.db import models

# Create your models here.
class Food(models.Model):
    foodID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    imageURL = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
