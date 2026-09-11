# Music Manager v1.1

A public music library manager built with **Django**.  
Browse, edit, and play songs with a dark Spotify-style UI.  
Deployed on **Render** with **Neon PostgreSQL** (production) and **SQLite** (local).

---

## Features 

# v1.1 Features 
- **Bottom player bar** — Stream audio via `yt-dlp` (YouTube search → direct audio URL)
- **Prefetch + cache** — Faster play, clean song switching, no ghost repeats

# v1.0 Features 
- **Library UI** — Master-detail layout (song table + edit panel)
- **Strict metadata** — Artists, genres, languages, tags only from DB (admin-controlled)
- **Searchable artists** — Tom Select multi-select dropdown
- **Add / Edit songs** — Full metadata form with checkboxes for genres/tags/languages
- **Django Admin** — Manage master lists (artists, genres, languages, tags)
- **Dual database** — Local SQLite for dev, Neon Postgres for production
- **Production ready** — WhiteNoise, Gunicorn, `dj-database-url`, `.env` secrets

---

## Tech Stack

| Layer      | Tech 
|------------|---------------
| Backend    | Django 6.1
| DB (local) | SQLite (`db.sqlite3`) 
| DB (prod)  | Neon PostgreSQL 
| Hosting    | Render 
| Player     | HTML5 `<audio>` + `yt-dlp` 

---

## Project Structure

```text
.
├── build.sh                 # Render build script
├── config/                  # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── songs/                   # Main app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/songs/
│       ├── songList.html    # Library + player UI
│       └── addSong.html     # Add song form
├── static/                  # Dev static assets
├── staticfiles/             # Collected static (prod)
├── media/                   # Uploaded media (if any)
├── templates/               # Project-level templates
├── docs/schema.txt          # DB schema notes
├── manage.py
├── requirements.txt
├── .env                     # Local secrets (not in git)
└── README.md