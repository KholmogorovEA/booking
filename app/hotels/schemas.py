from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from datetime import datetime


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[List[str]] = []
    image_id: int
    room_quantity: int
    created_at: datetime   # ПЕРЕДЕЛАТЬ под даты запросы
    rating: Optional[float] = None  # Сделаем поле необязательным
    data_from: Optional[str] = None  # Сделаем поле необязательным
    data_to: Optional[str] = None  # Сделаем поле необязательным

    class Config:
        from_attributes = True  # Включаем поддержку ORM моделей (SQLAlchemy)