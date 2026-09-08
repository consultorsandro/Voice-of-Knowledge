from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot

from voice_of_knowledge.core.conversion_pipeline import ConversionPipeline


class ConversionWorker(QObject):
    finished = Signal(list)
    error = Signal(str)
    progress = Signal(int, int, int)

    def __init__(
        self,
        input_file: str,
        output_dir: str,
        max_words: int,
    ) -> None:
        super().__init__()

        self.input_file = input_file
        self.output_dir = output_dir
        self.max_words = max_words

    def report_progress(
    self,
    current: int,
    total: int,
    word_count: int,
) -> None:
        self.progress.emit(
        current,
        total,
        word_count,
    )

    @Slot()
    def run(self) -> None:
        try:
            extension = Path(self.input_file).suffix.lower()

            if extension == ".txt":
                output_paths = ConversionPipeline.convert_txt_to_mp3(
                    self.input_file,
                    self.output_dir,
                    self.max_words,
                    self.report_progress,
                )

            elif extension == ".pdf":
                output_paths = ConversionPipeline.convert_pdf_to_mp3(
                    self.input_file,
                    self.output_dir,
                    self.max_words,
                )

            else:
                raise ValueError(
                    "Formato não suportado. Use arquivos TXT ou PDF."
                )

            self.finished.emit(output_paths)

        except Exception as exc:
            self.error.emit(str(exc))