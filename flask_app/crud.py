from typing import List
from fastapi import HTTPException
from requests import Session
import models, schemas


def get_all_contents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Content).offset(skip).limit(limit).all()

def get_content(db: Session, content_id: int):
    return db.query(models.Content).filter(models.Content.id == content_id).first()

def create_content(db: Session, contentSche: schemas.ContentCreate):
    db_content = models.Content(
        content=contentSche.content,
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def update_content(db: Session, content_id: int, content_update: schemas.ContentUpdate):
    db_content = db.query(models.Content).filter(models.Content.id == content_id).first()
    if not db_content:
        return None  # ถ้าไม่มี content ให้คืนค่า None

    # อัปเดตฟิลด์ที่ได้รับจาก content_update
    if content_update.content is not None:
        db_content.content = content_update.content

    db.commit()
    db.refresh(db_content)
    return db_content


def delete_content(db: Session, content_id: int):
    db_content = db.query(models.Content).filter(models.Content.id == content_id).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")

    db.delete(db_content)
    db.commit()
    return db_content  


def import_contents(db: Session, contents: List[schemas.ContentCreate]): 
     db.query(models.Content).delete()
     db.commit()

     for conts in contents:
         db_content = models.Content(content=conts[1])
         db.add(db_content)
         db.commit()
         db.refresh(db_content)

     all_Content= db.query(models.Content).all()

     return all_Content