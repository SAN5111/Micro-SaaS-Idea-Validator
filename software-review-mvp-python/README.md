# Software Review MVP

A minimal full-stack web app to list software products and collect reviews. Built with Python, FastAPI, SQLite, and Jinja2.

---

## Prerequisites

- Python 3.9+
- pip

## Quick start

```bash
cd software-review-mvp-python
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000** in your browser.

---

## What’s included

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | List all software; link to add new and open each product |
| Add Software | `/software/new` | Form: name, description, website (optional). On submit → home |
| Product detail | `/software/{id}` | Product info, website link, all reviews, average rating, form to add a review |

Reviews require: reviewer name, rating (1–5), and comment.

---

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/software` | List all software |
| `POST` | `/api/software` | Create software. Body: `{ "name", "description", "website?" }` |
| `GET` | `/api/software/{id}` | Get one software with its reviews |
| `POST` | `/api/reviews` | Create review. Body: `{ "softwareId", "name", "rating", "comment" }` |

---

## Database

- **SQLite** file: `software_review.db` in the project root (created on first run).
- Tables are created automatically at startup; no migrations to run.

## Tech stack

- **FastAPI** — web framework and API
- **SQLAlchemy** — ORM
- **SQLite** — database
- **Jinja2** — HTML templates (Tailwind CSS via CDN)
