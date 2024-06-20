from fastapi import APIRouter
from celery.result import AsyncResult

router = APIRouter()


@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == "PENDING":
        return {"task_id": task_id, "state": task_result.state, "status": "Pending..."}
    elif task_result.state != "FAILURE":
        return {
            "task_id": task_id,
            "state": task_result.state,
            "current": task_result.info.get("current", 0),
            "total": task_result.info.get("total", 1),
            "status": task_result.info.get("status", ""),
        }
    else:
        # something went wrong in the background job
        return {
            "task_id": task_id,
            "state": task_result.state,
            "status": str(task_result.info),  # this is the exception raised
        }
