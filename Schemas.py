from sqlalchemy import String, Column, DateTime, Integer
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

Base = declarative_base()





class User(Base):
    __tablename__ = "Users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[str] = mapped_column(String(40))
    password: Mapped[str] = mapped_column(String(150))
    username: Mapped[str] = mapped_column(String(50), unique=True)
    account_created = Column(DateTime, default=datetime.datetime.isoformat(datetime.datetime.now()))
    account_updated = Column(DateTime, default=datetime.datetime.isoformat(datetime.datetime.now()))
    access_token: Mapped[str] = mapped_column(String(100))



class Product(Base):

    __tablename__ = "Products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(100))
    sku: Mapped[str] = mapped_column(String(30))
    manufacturer: Mapped[str] = mapped_column(String(30))
    quantity: Mapped[int] = mapped_column(Integer)
    date_added = Column(DateTime, default=datetime.datetime.isoformat(datetime.datetime.now()))
    date_last_updated = Column(DateTime, default=datetime.datetime.isoformat(datetime.datetime.now()))
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users_table1.id"))
