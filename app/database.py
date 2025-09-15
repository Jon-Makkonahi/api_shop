# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, DeclarativeBase 


# # Строка подключения для SQLite
# DATABASE_URL = "sqlite:///ecommerce.db"

# # Создаём Engine
# engine = create_engine(DATABASE_URL, echo=True)

# # Настраиваем фабрику сеансов
# SessionLocal = sessionmaker(bind=engine)

# --------------- Асинхронное подключение к PostgreSQL -------------------------

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Строка подключения для SQLite
DATABASE_URL = "postgresql+asyncpg://user:pass@127.0.0.1:5432/db"

# Создаём Engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику сеансов
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


# Определяем базовый класс для моделей
class Base(DeclarativeBase):  # New
    pass
