from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import ModelFamily, ModelAlias, ModelVersion
from app.schemas import FamilyCreate, FamilyOut, VersionCreate, VersionOut, AliasOut
from app.services.search_service import record_search

router = APIRouter(prefix="/families", tags=["families"])

@router.get("/", response_model=List[FamilyOut])
def list_families(category: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(ModelFamily)
    if category: q = q.filter(ModelFamily.category == category)
    return q.order_by(ModelFamily.family_code).all()

@router.post("/", response_model=FamilyOut)
def create_family(family: FamilyCreate, db: Session = Depends(get_db)):
    db_family = ModelFamily(**family.dict())
    db.add(db_family)
    db.commit()
    db.refresh(db_family)
    return db_family

@router.get("/{family_id}", response_model=FamilyOut)
def get_family(family_id: int, db: Session = Depends(get_db)):
    f = db.query(ModelFamily).filter(ModelFamily.id == family_id).first()
    if not f: raise HTTPException(404, "Family not found")
    return f

@router.post("/{family_id}/aliases")
def add_alias(family_id: int, alias_code: str, alias_type: str = 'old', db: Session = Depends(get_db)):
    f = db.query(ModelFamily).filter(ModelFamily.id == family_id).first()
    if not f: raise HTTPException(404, "Family not found")
    alias = ModelAlias(family_id=family_id, alias_code=alias_code, alias_type=alias_type)
    db.add(alias)
    db.commit()
    return {"ok": True}

@router.get("/{family_id}/versions", response_model=List[VersionOut])
def list_versions(family_id: int, db: Session = Depends(get_db)):
    return db.query(ModelVersion).filter(ModelVersion.family_id == family_id).order_by(ModelVersion.created_at.desc()).all()

@router.post("/{family_id}/versions", response_model=VersionOut)
def create_version(family_id: int, version: VersionCreate, db: Session = Depends(get_db)):
    f = db.query(ModelFamily).filter(ModelFamily.id == family_id).first()
    if not f: raise HTTPException(404, "Family not found")
    db_version = ModelVersion(family_id=family_id, **version.dict())
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version
