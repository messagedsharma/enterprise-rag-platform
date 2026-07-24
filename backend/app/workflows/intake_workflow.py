from app.services.aws.bedrock_service import bedrock_service
from app.services.intake_service import intake_service
from app.services.pdf_extraction_service import pdf_extraction_service


class IntakeWorkflow:
    def start_intake(
        self,
        file_content: bytes,
        file_name: str,
        content_type: str,
    ) -> dict:
        intake = intake_service.intake_document(
            file_content=file_content,
            file_name=file_name,
            content_type=content_type,
        )

        intake_id = intake["intake_id"]

        intake_service.update_status(
            intake_id=intake_id,
            status="PROCESSING",
        )

        document_text = pdf_extraction_service.extract_text(
            file_content=file_content,
        )

        classification = bedrock_service.analyze_document(
            document_text=document_text,
        )

        intake_service.update_classification(
            intake_id=intake_id,
            document_type=classification["documentType"],
            confidence=classification["confidence"],
        )

        return intake_service.get_intake(intake_id)


intake_workflow = IntakeWorkflow()
