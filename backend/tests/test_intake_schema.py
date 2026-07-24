import unittest

from app.schemas.intake import IntakeResponse


class IntakeResponseTests(unittest.TestCase):
    def test_accepts_service_payload_and_serializes_api_fields(self):
        response = IntakeResponse(
            intake_id="intake-123",
            file_name="annual-report.pdf",
            status="UPLOADED",
            s3_key="intake/intake-123/original/annual-report.pdf",
        )

        self.assertEqual(
            response.model_dump(by_alias=True),
            {
                "intakeId": "intake-123",
                "fileName": "annual-report.pdf",
                "status": "UPLOADED",
                "s3Key": "intake/intake-123/original/annual-report.pdf",
            },
        )

    def test_accepts_workflow_payload(self):
        response = IntakeResponse(
            intakeId="intake-456",
            fileName="quarterly-report.pdf",
            status="Processing",
            s3Key="intake/intake-456/original/quarterly-report.pdf",
            createdAt="2026-07-24T05:07:08+00:00",
        )

        self.assertEqual(response.intake_id, "intake-456")
        self.assertEqual(response.file_name, "quarterly-report.pdf")
        self.assertEqual(
            response.model_dump(by_alias=True),
            {
                "intakeId": "intake-456",
                "fileName": "quarterly-report.pdf",
                "status": "Processing",
                "s3Key": "intake/intake-456/original/quarterly-report.pdf",
            },
        )


if __name__ == "__main__":
    unittest.main()
