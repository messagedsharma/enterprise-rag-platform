from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.intake import IntakeResponse
from app.services.s3_service import s3_service

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

    upload_id = str(uuid4())
    safe_file_name = Path(file.filename or "document.pdf").name

    object_key = (
        f"intake/{upload_id}/original/{safe_file_name}"
    )

    s3_service.upload_intake_document(
        file_content=file_content,
        object_key=object_key,
        content_type="application/pdf",
    )

    return IntakeResponse(
        upload_id=upload_id,
        file_name=safe_file_name,
        status="UPLOADED",
        s3_key=object_key,
    )
