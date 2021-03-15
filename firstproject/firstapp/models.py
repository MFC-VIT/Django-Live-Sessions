from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class MovieDetails(models.Model):
    name = models.CharField(max_length=260)
    dor = models.DateField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='movie_images')

    class Meta:
        verbose_name = 'Movie Details'
        verbose_name_plural = 'Movie Details'

    def __str__(self):
        return self.name

class MovieReviews(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    movie = models.ForeignKey(MovieDetails,on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    review = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Movie Review'
        verbose_name_plural = 'Movie Reviews'
        unique_together = ('user','movie')
        ordering = ['-date']

    def __str__(self):
        return 'Review for ' + self.movie.name + ' By ' + self.user.username + ' on ' + str(self.date)
