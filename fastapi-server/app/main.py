from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.infra.postgres.pool import db
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.infra.qdrant.client import qdrant
from app.core.logger import setup_logging, get_logger

setup_logging()  # dipanggil sekali, di main
logger = get_logger(__name__)  # dipanggil perfile


# ─────────────────────
# FastAPI Lifespan
# ─────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting TableauTalk application")

    # --- STARTUP ---
    await db.connect()
    logger.info("✅ PostgreSQL connection pool initialized")

    # # 🔍 TEST QUERY (INI YANG PENTING)
    # async with db.get_connection() as conn:
    #     value = await conn.fetchval("SELECT 1")
    #     logger.info(f"🟢 PostgreSQL test query result: {value}")

    qdrant.connect()
    logger.info("✅ Qdrant client initialized")

    yield  # ───── application is running ─────

    # --- SHUTDOWN ---
    logger.info("🧹 Shutting down TableauTalk application")
    await db.disconnect()
    logger.info("⏹️  PostgreSQL connection pool closed")


# ─────────────────────
# FastAPI App
# ─────────────────────
app = FastAPI(
    title="TableauTalk API",
    description=(
        "TableauTalk is an AI-powered analytics platform that allows users "
        "to explore data using natural language. "
        "It combines interactive data visualization, statistical analysis, "
        "and intelligent agents to generate insights from structured data."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


# ─────────────────────
# Middleware
# ─────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js
        "http://localhost:5173",  # Vite
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# ─────────────────────
# Routers (future)
# ─────────────────────
# from app.api.routes import auth, graph
# app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(graph.router, prefix="/graph", tags=["graph"])


# ─────────────────────
# Entrypoint
# ─────────────────────
def main() -> None:
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
