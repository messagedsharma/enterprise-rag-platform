from pydantic import BaseModel

class IntakeResponse(BaseModel):
    upload_id: str
    file_name: str
    status: str
    s3_key: str
