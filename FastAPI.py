
from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)


class ProductCreate(BaseModel):
    name: str
    description: str

class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    product_id: int
    name: str
    description: str

@app.post("/add_products/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(name=product.name, description=product.description)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/get_products/", response_model=List[ProductOut])
def get_product(db: Session = Depends(get_db)):
    db_products = db.query(Product).all()
    return db_products

@app.get("/get_products/{product_id}", response_model=ProductOut)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    return db_product

@app.put("/update_products/{product_id}", response_model=ProductOut)
def update_product(updated_product: ProductCreate, product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    db_product.name = updated_product.name
    db_product.description = updated_product.description
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/delete_products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    deleted_product_id = db_product.product_id
    db.delete(db_product)
    db.commit()
    return f"Deleted product ID: {deleted_product_id}"

