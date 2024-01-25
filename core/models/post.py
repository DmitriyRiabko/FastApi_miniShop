from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey

from .base import Base
from .mixins import UserRelationMixin



class Post(UserRelationMixin,Base):
    __tablename__ = 'posts'
    
    _user_back_populates ='posts'
    
    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(Text, default="", server_default="")
   
   
   
    def __str__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id}, title={self.title!r})'
    
    
    def __repr__(self) -> str:
        return str(self)