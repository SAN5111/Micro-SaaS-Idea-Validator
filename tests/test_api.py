import sys
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(str(Path(__file__).resolve().parents[1]))

from database import Base, get_db
from main import app


TEST_DB_URL = "sqlite:///./test_software_review.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_health_check():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_create_and_fetch_software():
    create_res = client.post(
        "/api/software",
        json={
            "name": "Notion",
            "description": "Docs and collaboration",
            "website": "https://notion.so",
        },
    )
    assert create_res.status_code == 200
    created = create_res.json()
    assert created["name"] == "Notion"
    assert created["reviewCount"] == 0
    assert created["averageRating"] is None

    list_res = client.get("/api/software")
    assert list_res.status_code == 200
    body = list_res.json()
    assert len(body) == 1
    assert body[0]["name"] == "Notion"


def test_duplicate_software_name_returns_409():
    payload = {
        "name": "Linear",
        "description": "Issue tracking",
        "website": "https://linear.app",
    }
    first = client.post("/api/software", json=payload)
    assert first.status_code == 200

    duplicate = client.post("/api/software", json=payload)
    assert duplicate.status_code == 409


def test_create_review_and_see_rating_summary():
    create_res = client.post(
        "/api/software",
        json={
            "name": "Figma",
            "description": "Design collaboration",
            "website": "https://figma.com",
        },
    )
    software_id = create_res.json()["id"]

    review_res = client.post(
        "/api/reviews",
        json={
            "softwareId": software_id,
            "name": "Sahana",
            "rating": 5,
            "comment": "Very productive workflow",
        },
    )
    assert review_res.status_code == 200

    detail_res = client.get(f"/api/software/{software_id}")
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert detail["reviewCount"] == 1
    assert detail["averageRating"] == 5.0
