from django.db import models

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=264)
    dor = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
