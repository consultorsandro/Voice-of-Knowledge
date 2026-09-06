import re
from pathlib import Path

import pymupdf


class PdfLoader:
    @staticmethod
    def _normalize_text(text: str) -> str:
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Une palavras quebradas por hífen no final da linha.
        # Exemplo:
        # conheci-
        # mento
        # vira:
        # conhecimento
        text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

        # Preserva separações reais de parágrafo.
        paragraphs = re.split(r"\n\s*\n", text)

        normalized_paragraphs = []

        for paragraph in paragraphs:
            lines = [
                line.strip()
                for line in paragraph.splitlines()
                if line.strip()
            ]

            if lines:
                normalized_paragraphs.append(" ".join(lines))

        return "\n\n".join(normalized_paragraphs).strip()

    @staticmethod
    def load(file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Arquivo PDF não encontrado: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                "O arquivo informado não possui extensão .pdf"
            )

        text_parts = []

        with pymupdf.open(path) as document:
            for page in document:
                page_text = page.get_text("text", sort=True)

                if page_text.strip():
                    normalized_page = PdfLoader._normalize_text(page_text)

                    if normalized_page:
                        text_parts.append(normalized_page)

        text = "\n\n".join(text_parts).strip()

        if not text:
            raise ValueError(
                "Não foi possível extrair texto do arquivo PDF"
            )

        return text