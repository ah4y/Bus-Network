# BusNet — CS50 Web Bus Network Lab

A Django web application for browsing and booking bus routes between stations, with user authentication.

## Features

### Core Features
- **Station & Route Models** — Station (name, city) and Route (origin FK, destination FK, duration, passengers M2M to User).
- **Authentication** — Register, login, and logout. Navbar shows username when logged in.
- **Index Page** — Lists all routes with origin, destination, duration, and passenger count.
- **Route Detail Page** — Shows route info, passenger list, and Book/Unbook buttons (login required).
- **Booking Logic** — POST-only book/unbook, restricted to authenticated users via `@login_required`.

### Bonus Features
- ✅ **My Routes** — A page showing all routes the logged-in user has booked.
- ✅ **Station Detail** — Page listing all routes departing from and arriving at a station.
- ✅ **Search/Filter** — Filter routes by station name or city from the index page.
- ✅ **Passenger Count** — Displayed next to each route on the index page.
- ✅ **Styled with Bootstrap** — Dark glassmorphism theme with Bootstrap 5, Inter font, and micro-animations.

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

## Known Limitations

- None at this time.
