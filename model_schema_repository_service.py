"""
Project structure overview:
models.py - SQLAlchemy model definition (Put inside Entity)
schemas.py - Pydantic schemas for validation (if using Entity this becomes Entity_Name/model.py)
repository.py - Data access layer with update operation (using Entity this becomes Entity_Name/controller.py - just call service layer methods with proper response_model,status_code)
service.py - Business logic layer

main.py - FastAPI controller with routes


"""
# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

# schemas.py
from pydantic import BaseModel
from typing import Optional

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ItemOut(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True

# repository.py
from sqlalchemy.orm import Session
from models import Item
from schemas import ItemUpdate

class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def update(self, item_id: int, item_update: ItemUpdate) -> Item:
        db_item = self.db.query(Item).filter(Item.id == item_id).first()
        if not db_item:
            return None
        update_data = item_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

# service.py
from repository import ItemRepository
from schemas import ItemUpdate
from models import Item
from sqlalchemy.orm import Session

class ItemService:
    def __init__(self, db: Session):
        self.repository = ItemRepository(db)

    def update_item(self, item_id: int, item_update: ItemUpdate) -> Item:
        updated_item = self.repository.update(item_id, item_update)
        if not updated_item:
            raise ValueError("Item not found")
        return updated_item

# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base
from schemas import ItemUpdate, ItemOut
from service import ItemService

DATABASE_URL = "sqlite:///./test.db"  # example sqlite connection
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.patch("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    service = ItemService(db)
    try:
        updated_item = service.update_item(item_id, item_update)
    except ValueError:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item