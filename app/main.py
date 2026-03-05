from fastapi import FastAPI, Depends,File, UploadFile
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models.photo import Photo
import os
import shutil
from datetime import datetime
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

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

@app.post("/upload-photo")
async def upload_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # uploads folder create if not exists
    os.makedirs("uploads", exist_ok=True)

    # unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    file_location = f"uploads/{timestamp}_{file.filename}"

    # save file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # save in DB
    new_photo = Photo(image_url=file_location)
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)

    return {
        "id": new_photo.id,
        "image_url": new_photo.image_url
    }

# python -m venv venv
# source venv/bin/activate
# venv\Scripts\activate
# pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv celery redis moviepy
# pip freeze > requirements.txt
# uvicorn app.main:app --reload