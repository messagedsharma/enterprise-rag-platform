import pymupdf


class PDFExtractionService:
    def extract_text(self, file_content: bytes) -> str:
        document = pymupdf.open(stream=file_content, filetype="pdf")

        pages = []

        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            if text.strip():
                pages.append(
                    f"\n--- PAGE {page_number} ---\n{text}"
                )

        document.close()

        return "\n".join(pages)


pdf_extraction_service = PDFExtractionService()
