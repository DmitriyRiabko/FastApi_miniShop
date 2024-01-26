from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .base import Base

class Order(Base):
   __tablename__ = 'orders'
   
   promocode: Mapped[str | None]
   created_at: Mapped[datetime] = mapped_column(
       server_default=func.now(),
       default=datetime.utcnow)
   
    
    