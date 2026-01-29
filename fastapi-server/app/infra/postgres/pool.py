import asyncpg
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager
from app.core.config import settings

class Database:
    def __init__(self) -> None:
        self._pool: Optional[asyncpg.Pool] = None

    async def connect(self) -> None:
        if not settings.POSTGRES_URL:
            raise RuntimeError("DATABASE_URL is not set")

        self._pool = await asyncpg.create_pool(settings.POSTGRES_URL)

    async def disconnect(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        if self._pool is None:
            raise RuntimeError("Database pool has not been initialized.")

        async with self._pool.acquire() as conn:
            yield conn # type: ignore


db = Database()

