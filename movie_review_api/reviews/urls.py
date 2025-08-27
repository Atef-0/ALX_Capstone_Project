from django.urls import path
from .views import MovieSearchView, MovieListView, MovieDetailView, ReviewListCreateView, ReviewDetailView


urlpatterns = [
    path("movies/search/", MovieSearchView.as_view(), name="movie-search"),
    path("movies/", MovieListView.as_view(), name="movie-list"),  
    path("movies/<int:id>/", MovieDetailView.as_view(), name="movie-detail"),
    path("reviews/", ReviewListCreateView.as_view(), name="review-list-create"),
    path("reviews/<int:id>/", ReviewDetailView.as_view(), name="review-detail"),
]