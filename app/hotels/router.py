from fastapi import APIRouter, Depends, Query
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.models import Users
from app.users.dependencies import get_current_user, get_admin_current_user
from datetime import date, datetime
from app.hotels.schemas import SHotels
from typing import List
from app.hotels.dao import HotelsDAO
from fastapi_cache.decorator import cache
import asyncio
from pydantic import parse_obj_as


router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)

@router.get("")
@cache(expire=30)
async def get_hotels_by_location_and_time(
    location: str,
    # data_from: date = Query(..., description=f"Пример, {datetime.now().date()}"),
    # data_to: date = Query(..., description=f"Пример, {datetime.now().date()}"),
):# -> List[SHotels]:
    await asyncio.sleep(1)
    hotels = await HotelsDAO.find_all_hotels(location)
    hotels_json = parse_obj_as(List[SHotels], hotels)
    return hotels_json  
