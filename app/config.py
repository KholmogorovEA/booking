from pydantic_settings import BaseSettings
from pydantic import BaseModel, model_validator, ConfigDict, root_validator
from typing import Literal

class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_URL: str = None #type: ignore 
    
    @root_validator(pre=True)
    def assemble_database_url(cls, values):
        if not values.get("DATABASE_URL"):
            values["DATABASE_URL"] = (
                f"postgresql+asyncpg://{values['DB_USER']}:{values['DATABASE_PASSWORD']}"
                f"@{values['DB_HOST']}:{values['DB_PORT']}/{values['DATABASE_NAME']}"
            )
        return values
    

    ##########################TEST_DB##################################


    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DATABASE_NAME: str
    TEST_DATABASE_PASSWORD: str
    TEST_DATABASE_URL: str = None  #type: ignore 

    @root_validator(pre=True)
    def assemble_test_database_url(cls, values):
        if not values.get("TEST_DATABASE_URL"):
            values["TEST_DATABASE_URL"] = (
                f"postgresql+asyncpg://{values['TEST_DB_USER']}:{values['TEST_DATABASE_PASSWORD']}"
                f"@{values['TEST_DB_HOST']}:{values['TEST_DB_PORT']}/{values['TEST_DATABASE_NAME']}"
            )
        return values




    SECRET_KEY: str           #для auth jwt token
    ALGORITHM: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = ".env"
    
settings = Settings() #type: ignore 

# Выводим значение DATABASE_URL
print(settings.DATABASE_URL)
