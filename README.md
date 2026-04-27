# BusNet 

A Django web application for browsing and booking bus routes between stations, with user authentication.

## Links

*(Note: Cloud deployment was skipped as an optional bonus per student preference; the app runs locally).*

## Features
# BusNet 

A Django web application for browsing and booking bus routes between stations, with user authentication.

## Links

**GitHub Repository:** [https://github.com/ah4y/busnet](https://github.com/ah4y/busnet)

## Features

### Core Features

- **Station & Route Models** — Station (name, city) and Route (origin FK, destination FK, duration, passengers M2M to User).
- **Authentication** — Register, login, and logout. Navbar shows username when logged in.
- **Index Page** — Lists all routes with origin, destination, duration, and passenger count.
- **Route Detail Page** — Shows route info, passenger list, and Book/Unbook buttons (login required).
- __Booking Logic__ — POST-only book/unbook, restricted to authenticated users via `@login_required`.

### Bonus Features

- ✅ **My Routes** — A page showing all routes the logged-in user has booked.
- ✅ **Station Detail** — Page listing all routes departing from and arriving at a station.
- ✅ **Search/Filter** — Filter routes by station name or city from the index page.
- ✅ **Passenger Count** — Displayed next to each route on the index page.
- ✅ **Styled with Bootstrap** — Bootswatch Brite theme with Bootstrap 5, Sora font, and bright UI cards.

## Tech Stack

- Python 3.12 / Django 6.0
- Bootstrap 5.3 (Bootswatch Brite theme)
- SQLite
- WhiteNoise for static files
- Gunicorn WSGI server
- Railway (Django app)

## Local Setup

```bash
cd busnet
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000

## Railway Deployment (Django)

1. Create a new Railway service from this repo.
2. Set environment variables:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS` (comma-separated, include your Railway domain)
   - `CSRF_TRUSTED_ORIGINS` (optional, comma-separated https origins)
3. Railway will use the Procfile to start Gunicorn.
4. Run static collection and migrations from the Railway console if needed:
   - `python manage.py collectstatic --noinput`
   - `python manage.py migrate`
