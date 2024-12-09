from datetime import date
from typing import Optional
# from datetime import time 
import time


from fastapi import Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.models import Users
from app.users.router import router as router_users
from app.logger import logger
import sentry_sdk
from fastapi_versioning import VersionedFastAPI, version
from prometheus_fastapi_instrumentator import Instrumentator

#####################################################


app = FastAPI()
sentry_sdk.init(
    dsn="",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)



app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)


origins = [
    "http://localhost:3000",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Authorization"],
    
)

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf-8", decode_response=True),
    FastAPICache.init(RedisBackend(redis), prefix="cache"), # type: ignore


# FastAPI versioning
app.version = "1.0.0"
app = VersionedFastAPI(app,
                       version_format='{major}',
                       prefix_format='/v{major}',
)


#metrics
instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"]
)
instrumentator.instrument(app).expose(app)


#Adminka sqlAdmin 
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time() #type: ignore
    response = await call_next(request)
    process_time = time.time() - start_time #type: ignore
    response.headers["X-Process-Time"] = str(process_time)
    # При подключении Prometheus + Grafana подобный лог не требуется
    logger.info("Request handling time", extra={   #type: ignore
        "process_time": round(process_time, 4)
    })
    return response



app.mount("/static", StaticFiles(directory="app/static"), "static") 