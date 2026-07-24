import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.config.settings import settings


class S3Service:
    def __init__(self) -> None:
        session = boto3.Session(
            profile_name=settings.aws_profile,
            region_name=settings.aws_region,
        )
        self.client = session.client("s3")

    def upload_intake_document(
            self,
            file_content: bytes,
            object_key: str,
            content_type: str,
    ) -> None:
        self.upload_file(
            file_content=file_content,
            object_key=object_key,
            content_type=content_type,
        )

    def upload_file(
        self,
        file_content: bytes,
        object_key: str,
        content_type: str,
    ) -> None:
        try:
            self.client.put_object(
                Bucket=settings.s3_bucket,
                Key=object_key,
                Body=file_content,
                ContentType=content_type,
            )
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError("Failed to upload document to S3") from exc


s3_service = S3Service()
