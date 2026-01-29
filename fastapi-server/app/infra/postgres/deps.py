from app.infra.postgres.pool import db
from collections.abc import AsyncGenerator
from asyncpg import Connection


# --------------------------------
# Database connection dependency
# --------------------------------
async def get_db_conn() -> AsyncGenerator[Connection, None]:
    async with db.get_connection() as conn:
        yield conn
