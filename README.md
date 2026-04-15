# Micro-SaaS Idea Validator

A simple full-stack app to submit software ideas, collect reviews, and check rating trends.

## Tech stack

- Python, FastAPI, SQLAlchemy
- SQLite
- Jinja2 templates + Tailwind CSS
- Pytest
- GitHub Actions for CI

## Features

- Submit software entries with name, description, and optional website
- Browse software list and open detail pages
- Add reviews with 1-5 ratings and comments
- Show `reviewCount` and `averageRating`
- REST API and server-rendered pages
- Duplicate-name check on software creation
- Health check endpoint

## Local setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000`.

## API endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET`  | `/api/health` | Service health check |
| `GET`  | `/api/software` | List software with rating summary |
| `POST` | `/api/software` | Create software |
| `GET`  | `/api/software/{id}` | Fetch one software with reviews |
| `POST` | `/api/reviews` | Create a review for a software item |

## Running tests

```bash
pytest -q
```
