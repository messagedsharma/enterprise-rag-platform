class BedrockService:
    def analyze_document(
        self,
        document_text: str,
    ) -> dict:
        normalized_text = document_text.lower()

        if "annual financial report" in normalized_text:
            return {
                "documentType": "ANNUAL_REPORT",
                "documentTypeConfidence": 0.99,
                "customerName": None,
                "customerNameConfidence": 0,
                "financialYear": None,
                "financialYearConfidence": 0,
                "industry": None,
                "industryConfidence": 0,
            }

        if "terms and conditions" in normalized_text:
            return {
                "documentType": "TERMS_DOCUMENT",
                "documentTypeConfidence": 0.95,
                "customerName": None,
                "customerNameConfidence": 0,
                "financialYear": None,
                "financialYearConfidence": 0,
                "industry": None,
                "industryConfidence": 0,
            }

        return {
            "documentType": "UNKNOWN",
            "documentTypeConfidence": 0.50,
            "customerName": None,
            "customerNameConfidence": 0,
            "financialYear": None,
            "financialYearConfidence": 0,
            "industry": None,
            "industryConfidence": 0,
        }


bedrock_service = BedrockService()
