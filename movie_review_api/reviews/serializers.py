from rest_framework import serializers
from .models import Review, Movie
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'year', 'director', 'created_at', 'poster_url', 'imdb_id']
        read_only_fields = ['id', 'created_at']



class ReviewCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), source='movie', write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie_id', 'user', 'rating', 'review_content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate_rating(self, value):
        if 1> value >10:
            raise serializers.ValidationError("Rating must be between 1 and 10.")
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)



class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'rating', 'review_content', 'created_at']
        read_only_fields = ['id', 'movie', 'user', 'created_at']

class ReviewListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'rating', 'review_content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'review_content']

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Rating must be between 1 and 10.")
        return value