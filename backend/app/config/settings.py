from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FinInsight AI"
    app_version: str = "1.0.0"

    aws_profile: str = "rag-project"
    aws_region: str = "us-east-1"

    s3_bucket: str = "fininsight-ai-document-442042537827-us-east-1-an"
    dynamodb_table: str = "customer-documents"
    dynamodb_intake_table: str
    processing_version: int = 1
    bedrock_model: str = "amazon.nova-lite-v2"

    class Config:
        env_file = ".env"

settings = Settings()
