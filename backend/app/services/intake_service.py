from uuid import uuid4

from app.repositories.intake_repository import intake_repository
from app.services.storage_service import storage_service


class IntakeService:
    def intake_document(
        self,
        file_content: bytes,
        file_name: str,
        content_type: str,
    ) -> dict:
        intake_id = str(uuid4())
        object_key = f"intake/{intake_id}/original/{file_name}"

        storage_service.upload_intake_document(
            file_content=file_content,
            object_key=object_key,
            content_type=content_type,
        )

        intake_repository.create_intake(
            intake_id=intake_id,
            file_name=file_name,
            s3_key=object_key,
        )

        return {
            "intake_id": intake_id,
            "file_name": file_name,
            "status": "UPLOADED",
            "s3_key": object_key,
        }

    def get_intake(self, intake_id: str) -> dict | None:
        return intake_repository.get_intake(intake_id)

    def update_status(
        self,
        intake_id: str,
        status: str,
    ) -> dict:
        return intake_repository.update_status(
            intake_id=intake_id,
            status=status,
        )

    def update_classification(
        self,
        intake_id: str,
        document_type: str,
        confidence: float,
    ) -> dict:
        return intake_repository.update_classification(
        intake_id=intake_id,
        document_type=document_type,
        confidence=confidence,
    )

intake_service = IntakeService()
