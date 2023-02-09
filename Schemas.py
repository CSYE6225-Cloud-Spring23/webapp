import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import String, Column, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(40), unique=True)
    account_created = Column(DateTime, default=datetime.datetime.isoformat(datetime.datetime.now()))
    account_updated = Column(DateTime, default=datetime.datetime.isoformat(datetime.datetime.now()))    


class Product(Base):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(100))
    sku: Mapped[str] = mapped_column(String(30))
    manufacturer: Mapped[str] = mapped_column(String(30))
    quantity: Mapped[int] = mapped_column(Integer)
    date_added = Column(DateTime, default=datetime.datetime.isoformat(datetime.datetime.now()))
    date_last_updated = Column(DateTime, default=datetime.datetime.isoformat(datetime.datetime.now()))
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    