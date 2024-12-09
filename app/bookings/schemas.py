from pydantic import BaseModel
from datetime import date


class SBooking(BaseModel):

    id: int
    room_id: int
    user_id: int
    data_from: date
    data_to: date
    price: int
    total_cost: int
    total_days: int

    class Config:
        from_attributes = True # сообщаем классу SBooking что у него есть атрибуты для pydentica
        # arbitrary_types_allowed = True # позволяем использовать не только обычные python-типы, но и SQLAlchemy-типы
        # json_encoders = {date: lambda d: d.isoformat()} # конвертируем даты в формат ISO 8601
