from sqlalchemy import JSON, Column, Integer, String, ForeignKey, Date, Computed
from datetime import datetime
from app.database import Base
from sqlalchemy.orm import relationship


class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    room_quantity = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    image_id = Column(Integer)
    created_at = Column(Date, nullable=False, default=datetime.utcnow())

    
    rooms = relationship("Rooms", back_populates="hotel")

    def __str__(self):
        return f"Отель {self.name} {self.location[0:30]}"


class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    image_id = Column(Integer)
    services = Column(JSON, nullable=False)
    quantity = Column(Integer, nullable=False)


    hotel = relationship("Hotels", back_populates="rooms")
    booking = relationship("Bookings", back_populates="room")

    def __str__(self):
        return f"Номер {self.name}"

