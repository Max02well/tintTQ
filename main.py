from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from app.config.settings import Settings
from app.config.database import engine, Base
from app.db.session import get_db
# from app.middleware.logging import LoggingMiddleware
# from app.middleware.rate_limit import RateLimitMiddleware
from app.routes import auth, booking, users, uploads, tint, ai, health, vehicle

logger = structlog.get_logger()

settings = Settings()

app = FastAPI(
    title="TintTQ AI",
    description="AI-Powered Car Tinting Platform",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json"
)

# Middleware
# app.add_middleware(LoggingMiddleware)
# app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
# app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
# app.include_router(uploads.router, prefix="/api/v1/uploads", tags=["Uploads"])
app.include_router(tint.router, prefix="/api/v1/tint", tags=["Tint"])
app.include_router(booking.router, prefix="/api/v1/bookings", tags=["Bookings"])
app.include_router(vehicle.router, prefix="/api/v1/vehicles", tags=["Vehicles"])
# app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI"])
# app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["Bookings"])

# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     logger.info("TintTQ AI started successfully")
@app.on_event("startup")
async def startup():
    logger.info("TintTQ AI started successfully")

@app.get("/")
async def root():
    return {"message": "Welcome to TintTQ AI 🚀"}
