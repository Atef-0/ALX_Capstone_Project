from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Review, Movie
from .serializers import ReviewSerializer, MovieSerializer, ReviewCreateSerializer, ReviewUpdateSerializer, ReviewListSerializer
from .services import OMDbService
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class MovieSearchView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MovieSerializer

    def get(self, request, format=None):
        title = request.query_params.get('title')
        year = request.query_params.get('year')
        if not title:
            return Response({"error": "Title parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        movie, created = OMDbService.get_or_create_movie(title)
        if not movie:
            return Response({"error": "Movie not found or could not be created."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class MovieListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['year', 'genre', 'director']
    search_fields = ['title', 'director', 'genre']
    ordering_fields = ['year', 'created_at']

class MovieDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    lookup_field = 'id'

class ReviewListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rating', 'movie__title', 'user__username']
    search_fields = ['review_content', 'movie__title', 'user__username']
    ordering_fields = ['rating', 'created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewListSerializer

    def get_queryset(self):
        return Review.objects.select_related('movie', 'user').all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        movie_title = request.data.get('movie_title')
        if not movie_title:
            return Response({"error": "movie_title is required."}, status=status.HTTP_400_BAD_REQUEST)
        movie, created = OMDbService.get_or_create_movie(movie_title)
        if not movie:
            return Response({"error": "Movie not found or could not be created."}, status=status.HTTP_404_NOT_FOUND)
        review_data = request.data.copy()
        review_data['movie_id'] = movie.id
        review_data['imdb_id'] = movie.imdb_id

        serializer = self.get_serializer(data=review_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Review.objects.select_related('movie', 'user').all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ReviewUpdateSerializer
        return ReviewSerializer

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.user:
            raise permissions.PermissionDenied("You do not have permission to edit this review.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise permissions.PermissionDenied("You do not have permission to delete this review.")
        instance.delete()
