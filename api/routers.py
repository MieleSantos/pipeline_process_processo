from v1.process.process import router as process_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(process_router, prefix="/process", tags=["process"])
