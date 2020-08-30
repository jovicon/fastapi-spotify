from sqlalchemy.orm import Session

import models, schemas

def get_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Result).offset(skip).limit(limit).all()

def create_results(db: Session, result: schemas.ResultCreate):
    db_result = models.Result( search=result.search, search_type=result.search_type, result=result.search_type )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result