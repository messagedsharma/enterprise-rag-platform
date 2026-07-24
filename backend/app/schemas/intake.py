from pydantic import BaseModel, ConfigDict, Field

class IntakeResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    intake_id: str = Field(alias="intakeId")
    file_name: str = Field(alias="fileName")
    status: str
    s3_key: str = Field(alias="s3Key")
