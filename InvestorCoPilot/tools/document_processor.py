import pdfplumber
from bs4 import BeautifulSoup


class DocumentProcessor:
    """Ingests PDF, HTML, or plain text financial documents."""

    def process(self, source: str) -> dict:
        if source.endswith(".pdf"):
            return self._process_pdf(source)
        elif source.endswith(".html") or source.startswith("http"):
            return self._process_html(source)
        return {"text": source, "source": "raw_text"}

    def _process_pdf(self, path: str) -> dict:
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return {"text": text, "source": path}

    def _process_html(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        return {"text": text, "source": "html"}
