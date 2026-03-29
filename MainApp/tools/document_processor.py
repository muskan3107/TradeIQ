"""
document_processor.py — Extracts text from PDF financial reports.

Receives a context dict from the agent, pulls the PDF path, and uses
pdfplumber to extract text page by page (capped at MAX_PAGES for demo
performance).  All failure modes return a consistent result dict so the
agent can continue without crashing.
"""

import os
from typing import Dict

import pdfplumber

MAX_PAGES = 30  # cap for demo performance


class DocumentProcessor:
    """
    Extracts text from a PDF file supplied via the agent context.

    Expected context shape:
        context = {
            'task_data': {
                'pdf_path': '/path/to/report.pdf'
            }
        }
    """

    def execute(self, context: Dict) -> Dict:
        """
        Main entry point called by the agent.

        Args:
            context: Agent context dict containing task_data.

        Returns:
            {
                'text':            str,   # concatenated page text
                'pages_extracted': int,   # pages successfully read
                'total_pages':     int,   # total pages in the PDF
                'success':         bool,
                'error':           str    # present only on failure
            }
        """
        # ── 1. Pull and validate the PDF path ─────────────────────────────────
        pdf_path = self._resolve_path(context)
        if pdf_path is None:
            return self._failure(
                "No PDF path provided. "
                "Expected context['task_data']['pdf_path'] to be a non-empty string.",
                pages_extracted=0,
                total_pages=0,
            )

        if not os.path.isfile(pdf_path):
            return self._failure(
                f"File not found: '{pdf_path}'. "
                "Check that the path is correct and the file exists.",
                pages_extracted=0,
                total_pages=0,
            )

        if not pdf_path.lower().endswith(".pdf"):
            return self._failure(
                f"Unsupported file type: '{os.path.basename(pdf_path)}'. "
                "Only .pdf files are accepted.",
                pages_extracted=0,
                total_pages=0,
            )

        # ── 2. Open and extract ───────────────────────────────────────────────
        return self._extract(pdf_path)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _extract(self, pdf_path: str) -> Dict:
        """Opens the PDF with pdfplumber and extracts text up to MAX_PAGES."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)

                if total_pages == 0:
                    return self._failure(
                        "The PDF contains no pages.",
                        pages_extracted=0,
                        total_pages=0,
                    )

                pages_to_read = pdf.pages[:MAX_PAGES]
                extracted_parts: list[str] = []
                pages_extracted = 0

                for i, page in enumerate(pages_to_read, start=1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            extracted_parts.append(page_text)
                        # Count the page even if it yielded no text (scanned image page)
                        pages_extracted += 1
                    except Exception as page_err:  # noqa: BLE001
                        # A single bad page should not abort the whole document
                        extracted_parts.append(
                            f"[Page {i} could not be read: {page_err}]"
                        )
                        pages_extracted += 1

                full_text = "\n\n".join(extracted_parts).strip()

                # ── Edge case: scanned PDF (images only, no selectable text) ──
                if not full_text:
                    return self._failure(
                        f"No extractable text found in '{os.path.basename(pdf_path)}' "
                        f"({pages_extracted} page(s) scanned). "
                        "The PDF may consist entirely of scanned images. "
                        "Consider running an OCR pre-processing step.",
                        pages_extracted=pages_extracted,
                        total_pages=total_pages,
                    )

                return {
                    "text":            full_text,
                    "pages_extracted": pages_extracted,
                    "total_pages":     total_pages,
                    "success":         True,
                }

        except pdfplumber.pdfminer.pdfparser.PDFSyntaxError as e:
            return self._failure(
                f"Corrupted or malformed PDF: {e}. "
                "The file may be incomplete or not a valid PDF.",
                pages_extracted=0,
                total_pages=0,
            )
        except PermissionError:
            return self._failure(
                f"Permission denied when opening '{pdf_path}'. "
                "Check file permissions.",
                pages_extracted=0,
                total_pages=0,
            )
        except Exception as e:  # noqa: BLE001
            return self._failure(
                f"Unexpected error while processing '{os.path.basename(pdf_path)}': "
                f"{type(e).__name__}: {e}",
                pages_extracted=0,
                total_pages=0,
            )

    @staticmethod
    def _resolve_path(context: Dict):
        """
        Safely navigates context['task_data']['pdf_path'].
        Returns the path string, or None if missing / not a string.
        """
        try:
            path = context["task_data"]["pdf_path"]
            return str(path).strip() if path and str(path).strip() else None
        except (KeyError, TypeError):
            return None

    @staticmethod
    def _failure(error: str, pages_extracted: int, total_pages: int) -> Dict:
        """Constructs a consistent failure result."""
        return {
            "text":            "",
            "pages_extracted": pages_extracted,
            "total_pages":     total_pages,
            "success":         False,
            "error":           error,
        }
