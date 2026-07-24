import importlib
import sys
import types
import unittest
from unittest.mock import Mock, patch


class IntakeWorkflowTests(unittest.TestCase):
    def test_passes_complete_analysis_to_service(self):
        intake_service = Mock()
        pdf_extraction_service = Mock()
        storage_service = Mock()
        bedrock_service = Mock()

        intake_service.intake_document.return_value = {
            "intake_id": "intake-123",
        }
        pdf_extraction_service.extract_text.return_value = (
            "Annual financial report"
        )
        analysis = {
            "documentType": "ANNUAL_REPORT",
            "documentTypeConfidence": 0.99,
            "customerName": None,
            "customerNameConfidence": 0,
            "financialYear": None,
            "financialYearConfidence": 0,
            "industry": None,
            "industryConfidence": 0,
        }
        bedrock_service.analyze_document.return_value = analysis
        intake_service.get_intake.return_value = {
            "intakeId": "intake-123",
            "status": "COMPLETED",
        }

        fake_modules = {
            "app.services.aws.bedrock_service": self._service_module(
                "bedrock_service", bedrock_service
            ),
            "app.services.intake_service": self._service_module(
                "intake_service", intake_service
            ),
            "app.services.pdf_extraction_service": self._service_module(
                "pdf_extraction_service", pdf_extraction_service
            ),
            "app.services.storage_service": self._service_module(
                "storage_service", storage_service
            ),
        }

        with patch.dict(sys.modules, fake_modules):
            sys.modules.pop("app.workflows.intake_workflow", None)
            module = importlib.import_module(
                "app.workflows.intake_workflow"
            )
            result = module.IntakeWorkflow().start_intake(
                file_content=b"pdf",
                file_name="annual-report.pdf",
                content_type="application/pdf",
            )

        intake_service.update_analysis.assert_called_once_with(
            intake_id="intake-123",
            analysis=analysis,
            extracted_text_key=(
                "intake/intake-123/extracted/annual-report.txt"
            ),
        )
        self.assertEqual(result["status"], "COMPLETED")

    @staticmethod
    def _service_module(attribute: str, service: Mock):
        module = types.ModuleType(attribute)
        setattr(module, attribute, service)
        return module


if __name__ == "__main__":
    unittest.main()
