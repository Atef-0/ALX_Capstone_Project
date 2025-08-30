# 🎬 Movie Reviews API
A secure REST API for discovering movies and managing user reviews — built with Django & Django REST Framework.

## 🌟 What is this?
The Movie Reviews API combines external data from the **OMDb API** with user-generated reviews. Users can search movies, view details, and create/update/delete their own reviews.

Perfect for:
- Building a React/Vue/mobile frontend for movies
- Learning how to integrate external APIs with Django REST Framework
- Creating a foundation for review-based applications

## ✨ Key Features
- User Authentication (JWT-based)
- Search movies via OMDb API
- View detailed movie information
- Create, update, and delete personal reviews
- Per-user review management (users can only edit/delete their own reviews)
- Clean RESTful API structure

## 🖥️ Demo Requests
### Search Movies
`GET /api/movies/search/?title=Inception`

### Get Movie Details
`GET /api/movies/<imdb_id>/`

### Create Review
`POST /api/reviews/`
```json
{
  "movie": "tt1375666",
  "rating": 5,
  "comment": "A mind-bending masterpiece!"
}
```

### Update Review
`PUT /api/reviews/<id>/`
```json
{
  "rating": 4,
  "comment": "Rewatched — still amazing!"
}
```

### Delete Review
`DELETE /api/reviews/<id>/`

### List User Reviews
`GET /api/reviews/`

## ⚡ Quick Start (Windows/Linux/Mac)
```bash
python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 📦 Models
### Review
```python
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    movie = models.CharField(max_length=20)  # imdb_id from OMDb
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## 📝 API Reference
| Method | Path                  | Auth | Description               |
|--------|-----------------------|------|---------------------------|
| GET    | /api/movies/search/   | ❌   | Search movies by title    |
| GET    | /api/movies/<imdb_id>/| ❌   | Movie details             |
| GET    | /api/reviews/         | ✅   | List user’s reviews       |
| POST   | /api/reviews/         | ✅   | Create new review         |
| GET    | /api/reviews/<id>/    | ✅   | Get specific review       |
| PUT    | /api/reviews/<id>/    | ✅   | Update a review           |
| DELETE | /api/reviews/<id>/    | ✅   | Delete a review           |

## 🛣️ Future Enhancements
- OpenAPI/Swagger documentation
- Review likes & comments
- Movie watchlist and favorites
- User profiles with activity stats

---

## 🌍 Deployed Endpoints

### 🔑 Accounts (Users)
- **Register** → `POST https://mohammedbadran.pythonanywhere.com/api/users/register/`
- **Login** → `POST https://mohammedbadran.pythonanywhere.com/api/users/login/`
- **Refresh Token** → `POST https://mohammedbadran.pythonanywhere.com/api/users/token/refresh/`
- **Logout** → `POST https://mohammedbadran.pythonanywhere.com/api/users/logout/`
- **Me** → `GET https://mohammedbadran.pythonanywhere.com/api/users/me/`

### 🎬 Movies
- **Search (example Batman)** → `GET https://mohammedbadran.pythonanywhere.com/api/movies/search/?title=Batman`
- **List** → `GET https://mohammedbadran.pythonanywhere.com/api/movies/`
- **Detail** → `GET https://mohammedbadran.pythonanywhere.com/api/movies/1/`

### 📝 Reviews
- **List Reviews** → `GET https://mohammedbadran.pythonanywhere.com/api/reviews/`
- **Create Review** → `POST https://mohammedbadran.pythonanywhere.com/api/reviews/`
- **Get Review by ID** → `GET https://mohammedbadran.pythonanywhere.com/api/reviews/1/`
- **Update Review (full)** → `PUT https://mohammedbadran.pythonanywhere.com/api/reviews/1/`
- **Update Review (partial)** → `PATCH https://mohammedbadran.pythonanywhere.com/api/reviews/1/`
- **Delete Review** → `DELETE https://mohammedbadran.pythonanywhere.com/api/reviews/1/`
