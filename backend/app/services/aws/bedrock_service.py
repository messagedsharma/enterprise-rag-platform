class BedrockService:
    def analyze_document(
        self,
        document_text: str,
    ) -> dict:
        normalized_text = document_text.lower()

        if "annual financial report" in normalized_text:
            return {
                "documentType": "ANNUAL_REPORT",
                "confidence": 0.99,
            }

        if "terms and conditions" in normalized_text:
            return {
                "documentType": "TERMS_DOCUMENT",
                "confidence": 0.95,
            }

        return {
            "documentType": "UNKNOWN",
            "confidence": 0.50,
        }


bedrock_service = BedrockService()
