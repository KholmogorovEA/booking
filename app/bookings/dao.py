from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from datetime import date
from app.bookings.schemas import SBooking
from sqlalchemy import select, insert, func, delete, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from app.database import async_session_maker, engine
from app.hotels.models import Hotels, Rooms
from fastapi import HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
from app.logger import logger

class BookingDAO(BaseDAO):

    model = Bookings

    @classmethod
    async def add1(cls, user_id, room_id, data_from, data_to):
        """
        WITH booked_rooms AS (
        SELECT * FROM bookings
        WHERE room_id = 1 AND
        (data_from >= '2024-05-15' AND data_from <= '2024-06-20') OR
        (data_from <= '2024-05-15' AND data_to > '2024-05-15')

        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """

        try:

            async with async_session_maker() as session:
                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
                            or_(
                                and_(
                                    Bookings.data_from >= data_from,
                                    Bookings.data_from <= data_to,
                                ),
                                and_(
                                    Bookings.data_from <= data_from,
                                    Bookings.data_to > data_from,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )

                """
                SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
                LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
                WHERE rooms.id = 1
                GROUP BY rooms.quantity, booked_rooms.room_id
                """

                get_rooms_left = (
                    select(
                        Rooms.quantity
                        - func.count(booked_rooms.c.room_id).label("rooms_left")
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )

                # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

                rooms_left_res = await session.execute(get_rooms_left)

                rooms_left: int = rooms_left_res.scalar() # type: ignore

                # проверка на свободные номера для бронирования
                if rooms_left == 0:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="На указанном диапазоне дат нет свободных номеров",
                    )

                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)   #select(Rooms.price).filter(Rooms.id == room_id)
                    price = await session.execute(get_price) # type: ignore
                    price: int = price.scalar() # type: ignore
                    add_booking = (
                        insert(Bookings)
                        .values(
                            user_id=user_id,
                            room_id=room_id,
                            data_from=data_from,
                            data_to=data_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()
                else:
                    return None
        except (SQLAlchemyError, Exception) as e:
             
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc:"
            elif isinstance(e, Exception):
                msg = "Unknown Exc:"
            msg += ": Cannot database"                             # type: ignore

            extra = {
             
                "user_id": user_id,
                "room_id": room_id,
                "data_from": data_from,
                "data_to": data_to,
            }
                
                
            logger.error(
                msg,#type: ignore
                extra=extra,
                exc_info=True,
            )#type: ignore