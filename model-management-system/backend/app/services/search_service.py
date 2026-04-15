from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import ModelFamily, ModelAlias, SearchHistory
from typing import List
from datetime import datetime

def search_families(db: Session, keyword: str, limit: int = 20) -> List[dict]:
    results = []
    families = db.query(ModelFamily).filter(
        or_(ModelFamily.family_code.ilike(f"%{keyword}%"),
            ModelFamily.family_name.ilike(f"%{keyword}%"))
    ).limit(limit).all()
    alias_families = db.query(ModelFamily).join(ModelAlias).filter(
        ModelAlias.alias_code.ilike(f"%{keyword}%")
    ).distinct().limit(limit).all()
    family_set = {f.id: f for f in families + alias_families}
    for f in list(family_set.values())[:limit]:
        aliases = [a.alias_code for a in f.aliases]
        results.append({
            "type": "family",
            "id": f.id,
            "main_code": f.family_code,
            "name": f.family_name,
            "aliases": aliases,
            "category": f.category
        })
    return results

def get_suggestions(db: Session, prefix: str, limit: int = 10) -> List[dict]:
    history = db.query(SearchHistory).filter(
        SearchHistory.search_term.ilike(f"{prefix}%")
    ).order_by(SearchHistory.search_count.desc()).limit(limit).all()
    suggestions = [{"term": h.search_term, "type": "history"} for h in history]
    families = db.query(ModelFamily).filter(
        or_(ModelFamily.family_code.ilike(f"{prefix}%"),
            ModelFamily.family_name.ilike(f"{prefix}%"))
    ).limit(limit - len(suggestions)).all()
    for f in families:
        suggestions.append({
            "term": f"{f.family_code} ({f.family_name})",
            "type": "model",
            "family_id": f.id
        })
    return suggestions[:limit]

def record_search(db: Session, keyword: str):
    if not keyword or len(keyword) < 2: return
    hist = db.query(SearchHistory).filter(SearchHistory.search_term == keyword).first()
    if hist:
        hist.search_count += 1
        hist.last_searched = datetime.now()
    else:
        db.add(SearchHistory(search_term=keyword))
    db.commit()
