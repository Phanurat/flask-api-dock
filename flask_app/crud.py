from typing import List
from requests import Session
import models, schemas


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