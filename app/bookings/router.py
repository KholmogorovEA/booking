from fastapi import APIRouter, Depends
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.models import Users
from app.users.dependencies import get_current_user, get_admin_current_user
from datetime import date
from pydantic import parse_obj_as
from app.tasks.tasks import send_booking_confirmation_email
from fastapi_versioning import version

router = APIRouter(
    prefix="/booking",
    tags=["Бронирование"],
)

@router.get("")
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    
    # print(user, type(user), user.email)
    return await BookingDAO.find_all(user_id=user.id) # type: ignore


@router.post("")
@version(1)
async def add_booking(
    room_id: int, data_from: date, data_to: date,
    user: Users = Depends(get_current_user),
    ):

    booking = await BookingDAO.add1(user.id, room_id, data_from, data_to)
    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_booking_confirmation_email.delay(booking_dict, user.email)               # type: ignore
    return booking_dict
