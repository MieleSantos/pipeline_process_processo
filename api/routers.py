from fastapi import APIRouter

from v1.router.process import router as process_router

router = APIRouter()
router.include_router(process_router, prefix="/process", tags=["process"])
