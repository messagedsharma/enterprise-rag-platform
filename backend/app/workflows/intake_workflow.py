from pathlib import Path
from app.services.aws.bedrock_service import bedrock_service
from app.services.intake_service import intake_service
from app.services.pdf_extraction_service import pdf_extraction_service
from app.services.storage_service import storage_service


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

        try:
            document_text = pdf_extraction_service.extract_text(
                file_content=file_content,
            )

            base_name = Path(file_name).stem
            extracted_text_key = (
                f"intake/{intake_id}/extracted/{base_name}.txt"
            )

            storage_service.upload_text(
                text=document_text,
                object_key=extracted_text_key
            )

            analysis = bedrock_service.analyze_document(
                document_text=document_text,
            )

            intake_service.update_analysis(
                intake_id=intake_id,
                analysis=analysis,
                extracted_text_key=extracted_text_key,
            )
        except Exception:
            intake_service.update_status(
                intake_id=intake_id,
                status="FAILED",
            )
            raise

        return intake_service.get_intake(intake_id)


intake_workflow = IntakeWorkflow()
