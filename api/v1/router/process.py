from celery.result import AsyncResult
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from v1.router.process_pdf import process_pdf_entity

router = APIRouter()


@router.get("/tasks/status/{task_id}", description="Get task status")
def get_task_status(task_id: str):
    result = AsyncResult(task_id)

    if result.state == "SUCCESS":
        print(result.info)
        return {"status": "SUCCESS", "csv_link": result.info}
    elif result.state == "FAILURE":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task failure.",
        )
    return {"status": result.state}


@router.post("/file", description="Process PDF file")
async def process_pdf(file_pdf: UploadFile = File(...)):
    if not file_pdf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid file",
        )

    try:
        resp = process_pdf_entity(file_pdf.file)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return resp
