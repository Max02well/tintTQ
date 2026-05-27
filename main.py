from fastapi import FastAPI
from app.routes.products import router as products_router
from app.routes.users import router as users_router
from app.middleware.timer import timing_middleware
# cors
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.middleware("http")(timing_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(products_router)
app.include_router(users_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the tintTQ API"}
