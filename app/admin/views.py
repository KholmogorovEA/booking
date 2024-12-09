from app.users.models import Users
from sqladmin import ModelView
from app.bookings.models import Bookings
from app.hotels.models import Hotels, Rooms


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.booking]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    column_details_exclude_list = [Users.hashed_password]


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user, Bookings.room]   #возврат всех имен колонок модели Букингов 
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"
   

class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.name]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.booking]
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-hotel"





