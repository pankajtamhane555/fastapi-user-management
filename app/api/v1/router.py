from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, rag

api_router = APIRouter()
# Add auth routes without any dependencies
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
# Add user routes with their own security dependencies
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(rag.router, prefix="/rag", tags=["rag"])

