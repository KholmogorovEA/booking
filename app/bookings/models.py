from sqlalchemy import JSON, Column, Integer, String, ForeignKey, Date, Computed
from app.database import Base
from sqlalchemy.orm import relationship


class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey("rooms.id"))
    user_id = Column(ForeignKey("users.id"))
    data_from = Column(Date, nullable=False)
    data_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed("((data_to - data_from) * price)", persisted=True))
    total_days = Column(Integer, Computed("(data_to - data_from)", persisted=True)) 

    user = relationship("Users", back_populates="booking")
    room = relationship("Rooms", back_populates="booking")

    def __str__(self):
        return f"Бронирование № {self.id}"