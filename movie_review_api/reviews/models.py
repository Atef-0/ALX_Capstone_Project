from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True, db_index=True)
    genre = models.CharField(max_length=100)
    year = models.CharField(max_length=12)
    director = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    poster_url = models.URLField(max_length=500, blank=True, null=True)
    imdb_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    rated = models.CharField(max_length=10, blank=True, null=True)
    director = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.title
    
class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10)
    ])
    review_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f'Review of {self.movie.title} by {self.user.username}'