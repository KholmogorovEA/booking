import pytest
from app.database import Base, async_session_maker, engine
from app.config import settings
from app.users.models import Users
from app.bookings.models import Bookings
from app.hotels.models import Hotels, Rooms
import json
from sqlalchemy import insert
import asyncio
from datetime import datetime
import aiofiles 


@pytest.fixture(scope="session", autouse=True)  #флаг для автоматич исполь текстуры перед нач кажд теста
async def test_abc():
    """
    Сперва важно убедиться через ассерт что мод это тестстовая среда 
    для работы с тестовой базой
    """
    assert settings.MODE == "TEST", "Нет подключения к TEST_DATABASE_URL >>>!"

    # создаем базу 
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # дропаем их все таблицы в базе 
        await conn.run_sync(Base.metadata.create_all)  # создаем все таблицы в базе 
        

    #Проверяем созданные таблицы
    from sqlalchemy import text
    result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
    tables = [row[0] for row in result]
    print("Созданные таблицы:", tables)


    # считываем файлы с данными для тест db
    async def open_mock(model: str):
        async with aiofiles.open(f"app/tests/mock_{model}.json", "r", encoding="utf-8") as file:
            content = await file.read()
            return json.loads(content)

    hotels = await open_mock("hotels")
    rooms = await open_mock("rooms")
    users = await open_mock("users")
    bookings = await open_mock("bookings")
    

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"],"%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"],"%Y-%m-%d")


    # загружаем тестовые данные в БД
    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)
        #print ...
        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)
        
        await session.commit()


# из оф докс к pytest-asyncio
@pytest.fixture(scope="session")  #запуск 1 раз для всех сессий тестов
def event_loop(request):
    """"Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

        


@pytest.fixture(scope="function")
def test():
    ...

    