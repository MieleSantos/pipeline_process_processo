from fastapi import APIRouter, File, UploadFile, HTTPException, status

from queue.tasks import process_pdf
from celery.result import AsyncResult
from queue.config import celery

router = APIRouter()


@router.post("/file")
async def task_pdf(file_pdf: UploadFile = File(...)):
    print(file_pdf)
    if not file_pdf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo invalido.",
        )

    try:
        file_content = await file_pdf.read()
        # print(file_content)
        # with open(f"{file_pdf.filename}", "wb") as f:
        #     f.write(file_content)

        task = process_pdf.delay(file_content)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    return {"task_id": task.id, "status": "Task sent to queue"}


@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery)
    if result.state == "SUCCESS":
        return {"task_id": task_id, "status": result.state, "result": result.result}
    return {"task_id": task_id, "status": result.state}
