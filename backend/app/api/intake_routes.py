from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel
from app.schemas.intake import IntakeResponse
from app.workflows.intake_workflow import intake_workflow
from app.services.intake_service import intake_service

router = APIRouter(prefix="/documents", tags=["Documents"])

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


@router.post("/intake", response_model=IntakeResponse)
async def intake_document(
    file: UploadFile = File(...),
) -> IntakeResponse:

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF documents are supported",
        )

    file_content = await file.read()

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty",
        )

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="The PDF exceeds the 20 MB limit",
        )

    safe_file_name = Path(file.filename or "document.pdf").name

    # result = intake_service.intake_document(
    #     file_content=file_content,
    #     file_name=safe_file_name,
    #     content_type="application/pdf",
    # )

    result = intake_workflow.start_intake(
        file_content=file_content,
        file_name=safe_file_name,
        content_type="application/pdf",
    )
    return IntakeResponse(**result)

@router.get("/intake/{intake_id}")
async def get_intake(intake_id: str):

    intake = intake_service.get_intake(intake_id)

    if intake is None:
        raise HTTPException(
            status_code=404,
            detail="Intake not found"
        )

    return intake

class IntakeStatusRequest(BaseModel):
    status: str

@router.patch("/intake/{intake_id}/status")
async def update_intake_status(
    intake_id: str,
    request: IntakeStatusRequest,
):
    try:
        return intake_service.update_status(
            intake_id=intake_id,
            status=request.status,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
