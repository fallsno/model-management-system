from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.database import engine, Base
from app.routers import families, versions, search

Base.metadata.create_all(bind=engine)

app = FastAPI(title="型号版本管理系统", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

uploads_dir = "uploads"
if not os.path.exists(uploads_dir): os.makedirs(uploads_dir)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

app.include_router(families.router, prefix="/api")
app.include_router(versions.router, prefix="/api")
app.include_router(search.router, prefix="/api")

@app.get("/")
def root(): return {"message": "Model Version Management API"}
