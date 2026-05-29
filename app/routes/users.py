from fastapi import APIRouter

router = APIRouter(tags=["users"])

@router.get("/", summary="Get all users")
async def get_users():
    return {"message": "List of users"}