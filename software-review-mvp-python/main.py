from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from crud import get_all_software, get_software_by_id, create_software, create_review
from schemas import SoftwareCreate, ReviewCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Software Review MVP", lifespan=lifespan)

templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


# ---------- Pages ----------

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    software = get_all_software(db)
    return templates.TemplateResponse(
        request, "home.html", {"software": software}
    )


@app.get("/software/new", response_class=HTMLResponse)
def add_software_page(request: Request):
    return templates.TemplateResponse(request, "software_new.html")


@app.post("/software/new")
def add_software_submit(
    request: Request,
    db: Session = Depends(get_db),
    name: str = Form(...),
    description: str = Form(...),
    website: str = Form(""),
):
    name = name.strip()
    description = description.strip()
    website = website.strip() or None
    if not name:
        raise HTTPException(status_code=400, detail="Name is required")
    if not description:
        raise HTTPException(status_code=400, detail="Description is required")
    create_software(db, name=name, description=description, website=website)
    return RedirectResponse(url="/", status_code=303)


@app.get("/software/{id}", response_class=HTMLResponse)
def software_detail(request: Request, id: str, db: Session = Depends(get_db)):
    software = get_software_by_id(db, id)
    if not software:
        raise HTTPException(status_code=404, detail="Software not found")
    reviews = sorted(software.reviews, key=lambda r: r.createdAt, reverse=True)
    avg_rating = (
        sum(r.rating for r in software.reviews) / len(software.reviews)
        if software.reviews else None
    )
    return templates.TemplateResponse(
        request,
        "software_detail.html",
        {
            "software": software,
            "reviews": reviews,
            "avg_rating": round(avg_rating, 1) if avg_rating is not None else None,
        },
    )


@app.post("/software/{id}/reviews")
def submit_review(
    id: str,
    db: Session = Depends(get_db),
    reviewer_name: str = Form(...),
    rating: int = Form(...),
    comment: str = Form(...),
):
    software = get_software_by_id(db, id)
    if not software:
        raise HTTPException(status_code=404, detail="Software not found")
    if not reviewer_name.strip():
        raise HTTPException(status_code=400, detail="Reviewer name is required")
    if rating not in (1, 2, 3, 4, 5):
        raise HTTPException(status_code=400, detail="Rating must be 1-5")
    if not comment.strip():
        raise HTTPException(status_code=400, detail="Comment is required")
    create_review(
        db,
        software_id=id,
        name=reviewer_name.strip(),
        rating=rating,
        comment=comment.strip(),
    )
    return RedirectResponse(url=f"/software/{id}", status_code=303)


# ---------- API ----------

@app.get("/api/software")
def api_list_software(db: Session = Depends(get_db)):
    software = get_all_software(db)
    return [
        {
            "id": s.id,
            "name": s.name,
            "description": s.description,
            "website": s.website,
            "createdAt": s.createdAt.isoformat() if s.createdAt else None,
        }
        for s in software
    ]


@app.post("/api/software")
def api_create_software(data: SoftwareCreate, db: Session = Depends(get_db)):
    s = create_software(
        db,
        name=data.name,
        description=data.description,
        website=data.website,
    )
    return {
        "id": s.id,
        "name": s.name,
        "description": s.description,
        "website": s.website,
        "createdAt": s.createdAt.isoformat() if s.createdAt else None,
    }


@app.get("/api/software/{id}")
def api_get_software(id: str, db: Session = Depends(get_db)):
    software = get_software_by_id(db, id)
    if not software:
        raise HTTPException(status_code=404, detail="Software not found")
    reviews = [
        {
            "id": r.id,
            "softwareId": r.softwareId,
            "name": r.name,
            "rating": r.rating,
            "comment": r.comment,
            "createdAt": r.createdAt.isoformat() if r.createdAt else None,
        }
        for r in software.reviews
    ]
    return {
        "id": software.id,
        "name": software.name,
        "description": software.description,
        "website": software.website,
        "createdAt": software.createdAt.isoformat() if software.createdAt else None,
        "reviews": reviews,
    }


@app.post("/api/reviews")
def api_create_review(data: ReviewCreate, db: Session = Depends(get_db)):
    software = get_software_by_id(db, data.softwareId)
    if not software:
        raise HTTPException(status_code=404, detail="Software not found")
    r = create_review(
        db,
        software_id=data.softwareId,
        name=data.name,
        rating=data.rating,
        comment=data.comment,
    )
    return {
        "id": r.id,
        "softwareId": r.softwareId,
        "name": r.name,
        "rating": r.rating,
        "comment": r.comment,
        "createdAt": r.createdAt.isoformat() if r.createdAt else None,
    }
