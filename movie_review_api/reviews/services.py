from django.core.cache import cache
from .models import Review
from django.conf import settings
import requests


class OMDbService:
    BASE_URL = settings.OMDb_URL
    API_KEY = settings.OMDb_API_KEY

    @classmethod
    def movie_search(cls, title):
        cache_key = f"omdb_search_{title.lower()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        params = {
            'apikey': cls.API_KEY,
            't': title,
            'type': 'movie'
        }

        try:
            response = requests.get(cls.BASE_URL, params = params)
            response.raise_for_status()
            data = response.json()
            if data.get('Response') == 'False':
                return f"Movie not found: {data.get('Error')}"
            cache.set(cache_key, data, timeout=3600)
        except requests.RequestException as e:
            print(f"Error retrieving data from OMDb API: {e}")
            return None
        
        