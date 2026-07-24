from pydantic import AliasChoices, BaseModel, ConfigDict, Field

class IntakeResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    intake_id: str = Field(alias="intakeId")
    file_name: str = Field(alias="fileName")
    status: str
    original_document_key: str = Field(
        validation_alias=AliasChoices(
            "originalDocumentKey",
            "s3Key",
            "s3_key",
        ),
        serialization_alias="originalDocumentKey",
    )
