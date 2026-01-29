import asyncpg
from datetime import datetime
from typing import Optional


class UserRepository:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    # --------------------------------------------------
    async def get_by_id(self, user_id: int) -> Optional[asyncpg.Record]:
        query = "SELECT * FROM users WHERE id = $1 LIMIT 1"
        return await self.conn.fetchrow(query, user_id)

    # --------------------------------------------------
    async def get_by_email(self, email: str) -> Optional[asyncpg.Record]:
        query = "SELECT * FROM users WHERE email = $1 LIMIT 1"
        return await self.conn.fetchrow(query, email)

    # --------------------------------------------------
    async def create_user(self, name: str, email: str, hashed_pwd: str) -> int:
        query = """
        INSERT INTO users (name, email, password, is_active, created_at)
        VALUES ($1, $2, $3, false, NOW())
        RETURNING id
        """
        return (await self.conn.fetchrow(query, name, email, hashed_pwd))["id"]  # type: ignore

    # --------------------------------------------------
    async def save_verification_token(
        self, user_id: int, token: str, expires_at: datetime
    ) -> None:
        query = """
        INSERT INTO email_verifications (user_id, token, expires_at, created_at)
        VALUES ($1, $2, $3, NOW())
        """
        await self.conn.execute(query, user_id, token, expires_at)

    # --------------------------------------------------
    async def get_user_by_verification_token(
        self, token: str
    ) -> Optional[asyncpg.Record]:
        query = """
        SELECT u.id AS user_id, u.email, u.is_active, u.name, v.expires_at
        FROM email_verifications v
        JOIN users u ON v.user_id = u.id
        WHERE v.token = $1
        LIMIT 1
        """
        return await self.conn.fetchrow(query, token)

    # --------------------------------------------------
    async def activate_user(self, user_id: int) -> None:
        query = "UPDATE users SET is_active = true WHERE id = $1"
        await self.conn.execute(query, user_id)

    # --------------------------------------------------
    async def delete_verification_token(self, token: str) -> None:
        query = "DELETE FROM email_verifications WHERE token = $1"
        await self.conn.execute(query, token)

    # --------------------------------------------------
    async def save_password_reset_token(
        self, user_id: int, token: str, expires_at: datetime
    ):
        query = """
        INSERT INTO password_resets (user_id, token, expires_at, created_at)
        VALUES ($1, $2, $3, NOW())
        """
        await self.conn.execute(query, user_id, token, expires_at)

    # --------------------------------------------------
    async def get_user_by_password_reset_token(self, token: str):
        query = """
        SELECT pr.user_id, pr.expires_at, u.email, u.name
        FROM password_resets pr
        JOIN users u ON u.id = pr.user_id
        WHERE pr.token = $1
        """
        return await self.conn.fetchrow(query, token)

    # --------------------------------------------------
    async def update_user_password(self, user_id: int, new_hashed_password: str):
        query = "UPDATE users SET password = $1 WHERE id = $2"
        await self.conn.execute(query, new_hashed_password, user_id)

    # --------------------------------------------------
    async def delete_password_reset_token(self, token: str):
        query = "DELETE FROM password_resets WHERE token = $1"
        await self.conn.execute(query, token)
