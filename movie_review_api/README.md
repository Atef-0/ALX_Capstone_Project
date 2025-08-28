# Movie Review API

A Django REST Framework project for browsing movies and posting reviews.  
Integrates with the OMDb API to fetch movie details.

---

## Features
- Search movies using the OMDb API
- View movie details
- Add, update (PATCH), and delete reviews
- User authentication (register, login, logout, refresh token)
- Protected routes for user actions

---

## Tech Stack
- Django & Django REST Framework
- SQLite (development)
- OMDb API

---

## API Endpoints

### Movies
- `GET /api/movies/search/` → Search movies  
- `GET /api/movies/` → List movies  
- `GET /api/movies/<id>/` → Movie details  

### Reviews
- `GET /api/reviews/` → List reviews / create review  
- `POST /api/reviews/` → Add a review  
- `GET /api/reviews/<id>/` → Review details  
- `PATCH /api/reviews/<id>/` → Update review  
- `DELETE /api/reviews/<id>/` → Delete review  

### Users
- `POST /api/register/` → Register a new user  
- `POST /api/login/` → Login and get token  
- `POST /api/token/refresh/` → Refresh token  
- `POST /api/logout/` → Logout  
- `GET /api/me/` → Get current user profile  

---
