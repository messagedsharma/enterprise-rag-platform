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
        s3_key: str,
    ) -> None:
        try:
            self.table.put_item(
                Item={
                    "intakeId": intake_id,
                    "fileName": file_name,
                    "s3Key": s3_key,
                    "status": "UPLOADED",
                    "createdAt": datetime.now(timezone.utc).isoformat(),
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

    def update_classification(
        self,
        intake_id: str,
        document_type: str,
        confidence: float,
    ) -> dict:
        response = self.table.update_item(
        Key={"intakeId": intake_id},
        UpdateExpression=(
            "SET documentType = :document_type, "
            "classificationConfidence = :confidence, "
            "#status = :status"
        ),
        ExpressionAttributeNames={
            "#status": "status",
        },
        ExpressionAttributeValues={
            ":document_type": document_type,
            ":confidence": Decimal(str(confidence)),
            ":status": "CLASSIFIED",
        },
        ConditionExpression="attribute_exists(intakeId)",
        ReturnValues="ALL_NEW",
    )

        return response["Attributes"]

intake_repository = IntakeRepository()
