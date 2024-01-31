from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
   from .order import Order



class Product(Base):
   __tablename__ = 'products'
   
   name: Mapped[str]
   description: Mapped[str]
   price: Mapped[int]
   
   
   orders: Mapped[list['Order']] =relationship(
       secondary='order_product_association',
       back_populates='products'
   )
   
   
    
    