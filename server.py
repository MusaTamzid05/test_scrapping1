from fastapi import FastAPI, Depends, Query, HTTPException
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, desc
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

app = FastAPI()

DATABASE_URL = "postgresql://myuser:mypassword@localhost/mydatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = 'watches'
    
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    model = Column(String)
    price = Column(Float)
    rating = Column(Float)
    specifications = Column(String)
    image_url = Column(String)

    reviews = relationship("Review", back_populates="product")


class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, index=True)
    watch_id = Column(Integer, ForeignKey('watches.id'))
    rating = Column(Float)
    review_text = Column(String)
    reviewer_name = Column(String)

    product = relationship("Product", back_populates="reviews")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def paginate(query, page: int, limit: int):
    return query.offset((page - 1) * limit).limit(limit).all()


@app.get("/products")
def get_products(
    brand: Optional[str] = None,
    model: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    sort_by: Optional[str] = "price",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    
    # Apply search filters
    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))
    if model:
        query = query.filter(Product.model.ilike(f"%{model}%"))
    
    # Apply price and rating filters
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    if min_rating:
        query = query.filter(Product.rating >= min_rating)
    
    # Sorting
    if sort_by == "price":
        query = query.order_by(Product.price)
    elif sort_by == "rating":
        query = query.order_by(desc(Product.rating))
    
    # Pagination
    products = paginate(query, page, limit)
    return products


# Endpoint 2: GET /products/top (top products based on rating and reviews)
@app.get("/products/top")
def get_top_products(
    db: Session = Depends(get_db)
):
    top_products = db.query(Product).order_by(desc(Product.rating)).limit(5).all()

    result = []
    for product in top_products:
        product_data = {
            "id": product.id,
            "brand": product.brand,
            "model": product.model,
            "price": product.price,
            "rating": product.rating,
            "reviews": [{"review_text": review.review_text, "reviewer_name": review.reviewer_name} for review in product.reviews]
        }
        result.append(product_data)
    
    return result


# Endpoint 3: GET /products/{product_id}/reviews (reviews for a specific product with pagination)
@app.get("/products/{product_id}/reviews")
def get_product_reviews(
    product_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    reviews_query = db.query(Review).filter(Review.watch_id== product_id)
    reviews = paginate(reviews_query, page, limit)
    
    return reviews


