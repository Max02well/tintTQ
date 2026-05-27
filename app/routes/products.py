from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["products"])

@router.get("/products")
async def get_products():
    return {"message": "List of products"}