import crud, models, schemas, csv, io
from fastapi import FastAPI, Depends, File,HTTPException, Response, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine

from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"iron": "v.1"}

@app.get("/content", response_model=list[schemas.Contents])
def read_all_content(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contents = crud.get_all_contents(db, skip=skip, limit=limit)
    return contents

@app.get("/content/{content_id}", response_model=schemas.Contents)
def read_content(content_id: int, db: Session = Depends(get_db)):
    db_content= crud.get_content(db=db, content_id=content_id)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content


@app.post("/content", response_model=schemas.Contents)
def create_content(contents: schemas.ContentCreate, db: Session = Depends(get_db)):
    # ตรวจสอบว่ามีการส่ง Content มาหรือไม่
    if not contents.content:
        raise HTTPException(status_code=400, detail="Contents are required")

    return crud.create_content(db=db, contentSche=contents)


@app.put("/update/content/{content_id}", response_model=schemas.Contents)
def content_update(content_id: int, content_update: schemas.ContentUpdate, db: Session = Depends(get_db)):
    if not content_update.content:
        raise HTTPException(status_code=400, detail="content are required")

    db_content = crud.update_content(db=db, content_id=content_id, content_update=content_update)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content

@app.delete("/delete/content/{content_id}", status_code=204)
def delete_content(content_id: int, db: Session = Depends(get_db)):
    db_content = crud.delete_content(db=db, content_id=content_id)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return Response(status_code=204)  # No content to return


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



