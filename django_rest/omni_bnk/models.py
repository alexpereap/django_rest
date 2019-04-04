from django.db import models

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    year = models.CharField(max_length=20)
    recommended = models.BooleanField()

    def __str__(self):
        return self.name