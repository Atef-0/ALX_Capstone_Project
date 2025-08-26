from django.core.cache import cache
from .models import Review, Movie
from django.conf import settings
import requests


class OMDbService:
    BASE_URL = settings.OMDb_URL
    API_KEY = settings.OMDb_API_KEY

    @staticmethod
    def validate_year(year):
        year_int = int(year)
        if year_int and 1800 <= int(year) <= 2100:
            return True
        return False

    @classmethod
    def movie_search(cls, title, *args, **kwargs):
        cache_key = f"omdb_search_{title.lower()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        params = {
            'apikey': cls.API_KEY,
            't': title,
            'type': 'movie'
        }

        year = kwargs.get('year')
        if year and cls.validate_year(year):
            params['y'] = year

        try:
            response = requests.get(cls.BASE_URL, params = params)
            response.raise_for_status()
            data = response.json()
            if data.get('Response') == 'False':
                return f"Movie not found: {data.get('Error')}"
            cache.set(cache_key, data, timeout=3600)
            return data
        except requests.RequestException as e:
            print(f"Error retrieving data from OMDb API: {e}")
            return None
        
    
    @classmethod
    def get_or_create_movie(cls, title):
        try:
            movie = Movie.objects.get(title__iexact=title)
            return movie, False
        except Movie.DoesNotExist:
            pass

        movie_data = cls.movie_search(title)
        if not movie_data or 'Error' in movie_data:
            return None, False
        
        movie = Movie(
            title=movie_data.get('Title'),
            year=movie_data.get('Year'),
            rated=movie_data.get('Rated'),
            genre=movie_data.get('Genre'),
            director=movie_data.get('Director'),
            language=movie_data.get('Language'),
            poster_url=movie_data.get('Poster'),
            imdb_id=movie_data.get('imdbID'),
            type=movie_data.get('Type'),
        )
        movie.save()
        return movie, True
    