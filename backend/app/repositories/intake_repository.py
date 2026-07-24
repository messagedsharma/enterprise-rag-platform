from datetime import datetime, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.config.settings import settings
from decimal import Decimal

class IntakeRepository:
    def __init__(self) -> None:
        session = boto3.Session(
            profile_name=settings.aws_profile,
            region_name=settings.aws_region,
        )
        dynamodb = session.resource("dynamodb")
        self.table = dynamodb.Table(settings.dynamodb_intake_table)

    def create_intake(
        self,
        intake_id: str,
        file_name: str,
        original_document_key: str,
    ) -> None:
        try:
            created_at = datetime.now(timezone.utc).isoformat()
            self.table.put_item(
                Item={
                    "intakeId": intake_id,
                    "fileName": file_name,
                    "originalDocumentKey": original_document_key,
                    "processingVersion": settings.processing_version,
                    "bedrockModel": settings.bedrock_model,
                    "status": "IN_PROGRESS",
                    "workflowStage": "INTAKE_METADATA_EXTRACTION",
                    "createdAt": created_at,
                    "updatedAt": created_at,
                },
                ConditionExpression="attribute_not_exists(intakeId)",
            )
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError("Failed to create intake record") from exc


    def get_intake(self, intake_id: str):
        response = self.table.get_item(
            Key={
                "intakeId": intake_id
        }
    )
        return response.get("Item")

    def update_status(
        self,
        intake_id: str,
        status: str,
    ) -> dict:
        try:
            response = self.table.update_item(
                Key={
                    "intakeId": intake_id,
                },
            UpdateExpression=(
                "SET #status = :status, "
                "updatedAt = :updated_at"
            ),
            ExpressionAttributeNames={
                "#status": "status",
            },
            ExpressionAttributeValues={
                ":status": status,
                ":updated_at": datetime.now(timezone.utc).isoformat(),
            },
            ConditionExpression="attribute_exists(intakeId)",
            ReturnValues="ALL_NEW",
        )

            return response["Attributes"]

        except self.table.meta.client.exceptions.ConditionalCheckFailedException:
            raise ValueError("Intake not found")

        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError("Failed to update intake status") from exc

    def update_analysis(
        self,
        intake_id: str,
        analysis: dict,
        extracted_text_key: str,
    ) -> dict:
        metadata_extracted_at = datetime.now(timezone.utc).isoformat()

        response = self.table.update_item(
            Key={"intakeId": intake_id},
            UpdateExpression=(
                "SET documentType = :document_type, "
                "customerName = :customer_name, "
                "financialYear = :financial_year, "
                "industry = :industry, "
                "documentTypeConfidence = :document_type_confidence, "
                "customerNameConfidence = :customer_name_confidence, "
                "financialYearConfidence = :financial_year_confidence, "
                "industryConfidence = :industry_confidence, "
                "extractedTextKey = :extracted_text_key, "
                "metadataExtractedAt = :metadata_extracted_at, "
                "updatedAt = :updated_at, "
                "workflowStage = :workflow_stage, "
                "#status = :status"
            ),
            ExpressionAttributeNames={
                "#status": "status",
            },
            ExpressionAttributeValues={
                ":document_type": analysis.get("documentType"),
                ":customer_name": analysis.get("customerName"),
                ":financial_year": analysis.get("financialYear"),
                ":industry": analysis.get("industry"),
                ":document_type_confidence": Decimal(
                    str(analysis.get("documentTypeConfidence", 0))
                ),
                ":customer_name_confidence": Decimal(
                    str(analysis.get("customerNameConfidence", 0))
                ),
                ":financial_year_confidence": Decimal(
                    str(analysis.get("financialYearConfidence", 0))
                ),
                ":industry_confidence": Decimal(
                    str(analysis.get("industryConfidence", 0))
                ),
                ":extracted_text_key": extracted_text_key,
                ":metadata_extracted_at": metadata_extracted_at,
                ":updated_at": metadata_extracted_at,
                ":workflow_stage": "INTAKE_METADATA_EXTRACTION",
                ":status": "READY_FOR_NEXT_STAGE",
            },
            ConditionExpression="attribute_exists(intakeId)",
            ReturnValues="ALL_NEW",
        )

        return response["Attributes"]



intake_repository = IntakeRepository()
