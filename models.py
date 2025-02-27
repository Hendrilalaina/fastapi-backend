from sqlalchemy import Column, Integer, String, Float
from database import Base
from uuid import uuid4

class Product(Base):
    __tablename__ = "products"
    id = Column(String(36),default=uuid4, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(255))
    price = Column(Float)