from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import schemas
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
  "http://localhost:8080",
  "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.post('/product')
async def add(request: schemas.Product, db: Session=Depends(get_db)):
  product = models.Product()
  product.name = request.name
  product.description = request.description
  product.price = request.price

  db.add(product)
  db.commit()
  return request

@app.get("/products")
async def get_all(db: Session=Depends(get_db)):
  return db.query(models.Product).all()

@app.get("/product/{product_id}")
async def get_product(product_id: int, db: Session=Depends(get_db)):
  product_model = db.query(models.Product).filter(models.Product.id == product_id).first()
  if product_model is not None:
    return product_model
  raise http_exception()

@app.delete("/product/{product_id}")
async def delete_product(product_id: int, db: Session=Depends(get_db)):
  product_model = db.query(models.Product).filter(models.Product.id == product_id).first()
  if product_model is None:
    raise http_exception()
  
  db.query(models.Product).filter(models.Product.id == product_id).delete()
  db.commit()
  return {
    'status': 201,
    'transaction': 'Success'
  }

@app.put("/product/{product_id}")
async def update_product(product_id: int, product: schemas.Product, db: Session=Depends(get_db)):
  product_model = db.query(models.Product).filter(models.Product.id == product_id).first()
  if product_model is None:
    raise http_exception()
  
  product_model.description = product.description
  product_model.name = product.name
  product_model.price = product.price

  db.add(product_model)
  db.commit()
  return {
    'status': 200,
    'transaction': 'Success'
  }

@app.post("/filter")
async def filter_post(request: dict, db: Session=Depends(get_db)):
  product_model = db.query(models.Product).\
                  filter(models.Product.name.like(str("%" + request['name'] + "%")) |
                  models.Product.price.between(request['min_price'], request['max_price'])).\
                  all()
  return product_model

def http_exception():
  return HTTPException(status_code=404, detail="Product not found")