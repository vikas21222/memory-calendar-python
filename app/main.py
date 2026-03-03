from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models.photo import Photo

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "DB Connected 🚀"}

@app.post("/photos")
async def create_photo(image_url: str, db: Session = Depends(get_db)):
    new_photo = Photo(image_url=image_url)

    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)

    return {
        "id": new_photo.id,
        "image_url": new_photo.image_url,
        "upload_date": new_photo.upload_date
    }

@app.get("/photos")
async def get_photos(db: Session = Depends(get_db)):
    photos = db.query(Photo).all()

    return [
        {
            "id": photo.id,
            "image_url": photo.image_url,
            "upload_date": photo.upload_date
        }
        for photo in photos
    ]


# python -m venv venv
# source venv/bin/activate
# venv\Scripts\activate
# pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv celery redis moviepy
# pip freeze > requirements.txt
# uvicorn app.main:app --reload