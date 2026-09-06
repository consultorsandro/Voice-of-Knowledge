from pathlib import Path


class TextLoader:
    @staticmethod
    def load(file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        if not path.is_file():
            raise ValueError(f"O caminho informado não é um arquivo: {path}")

        return path.read_text(encoding="utf-8")