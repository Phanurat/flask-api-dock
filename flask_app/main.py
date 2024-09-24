import csv
import io
from fastapi import FastAPI, Depends, File,HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import crud
from database import SessionLocal, engine
import models

from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "http://localhost:3000",
    'http://127.0.0.1:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"iron": "v.1"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/content/")
def read_all_content(db: Session = Depends(get_db)):
    contents = db.query(models.Content).all()
    return contents

@app.get("/content/{content_id}")
def read_content(content_id: int, db: Session = Depends(get_db)):
    return db.query(models.Content).filter(models.Content.id == content_id).first()

@app.post("/content/")
def create_content(content: str, db: Session = Depends(get_db)):
    db_comment = models.Content(content=content)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@app.put("/update/content/{content_id}")
def update_content(content_id: int, content_update: str, db: Session = Depends(get_db)):
    db_comment = db.query(models.Content).filter(models.Content.id == content_id).first()
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Content not found")
    db_comment.content = content_update
    db.commit()
    db.refresh(db_comment)
    return db_comment

@app.delete("/delete/content/{content_id}")
def delete_content(content_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(models.Content).filter(models.Content.id == content_id).first()
    
    if not db_comment:
        raise HTTPException(status_code=404, detail="Content not found")
    
    db.delete(db_comment)
    db.commit()
    
    return {"detail": "Content deleted successfully"}


@app.get("/contents/export")
async def export_contents(db: Session = Depends(get_db)):
    
    contents = db.query(models.Content).all()
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["id", "content"])

    for conts in contents:
        writer.writerow([conts.id, conts.content])

    buffer.seek(0)

    return StreamingResponse(buffer, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=contents.csv"
    })

@app.post("/contents/import")
async def update_contents_from_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):

    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

    contents = await file.read()
    csv_reader = csv.reader(io.StringIO(contents.decode("utf-8")))

    # remove header
    header = next(csv_reader)

    updated_contents = crud.import_contents(db, csv_reader)

    return {"detail": "updated successfully", "updated_data": updated_contents}



