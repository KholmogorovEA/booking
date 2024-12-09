from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from datetime import date
from app.bookings.schemas import SBooking
from sqlalchemy import select, insert, func, delete, and_, or_
from app.database import async_session_maker, engine
from app.hotels.models import Hotels, Rooms
from fastapi import HTTPException, status

class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all_hotels(cls, location: str):
        async with async_session_maker() as session:
            # Используем фильтрацию через where
            query = select(cls.model).where(
                and_(
                    cls.model.location.ilike(f"%{location}%"),
                  
                   
                    # cls.model.created_at >= data_from,
                    # cls.model.created_at <= data_to
                    
                )
            )
            result = await session.execute(query)
            
            if not result:
                print("404")
            return result.scalars().all()