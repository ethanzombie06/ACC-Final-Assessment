from sqlalchemy import Integer, String, DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_login import UserMixin

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Users(db.Model,UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    Username: Mapped[str] = mapped_column(String(13))
    Email: Mapped[str] = mapped_column(String(25),unique=True)
    Password: Mapped[str]

class Bookings(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    Booking_type: Mapped[str]
    Email: Mapped[str] = mapped_column(String(13))
    Attendees: Mapped[int]
    Start: Mapped[str]
    End: Mapped[str]

class Content(db.Model):
    Content_Id: Mapped[int]= mapped_column(primary_key=True)
    Title: Mapped[str]
    Img: Mapped[str]
    Body: Mapped[str]