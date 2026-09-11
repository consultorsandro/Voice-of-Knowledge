from pathlib import Path
from threading import Event

from PySide6.QtCore import QObject, Signal, Slot

from voice_of_knowledge.core.conversion_pipeline import ConversionPipeline


class ConversionWorker(QObject):
    finished = Signal(list)
    cancelled = Signal(list)
    error = Signal(str)
    progress = Signal(int, int, int)
    
    def __init__(
        self,
        input_file: str,
        output_dir: str,
        max_words: int,
        voice: str = "pm_alex",
    ) -> None:
        super().__init__()

        self.input_file = input_file
        self.output_dir = output_dir
        self.voice = voice
        self.max_words = max_words
        self._cancel_event = Event()
        self._cancel_acknowledged = False

    def request_cancel(self) -> None:
        self._cancel_event.set()

    def is_cancel_requested(self) -> bool:
        if self._cancel_event.is_set():
          self._cancel_acknowledged = True
          return True

        return False

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
                   input_path=self.input_file,
                   output_dir=self.output_dir,
                   max_words=self.max_words,
                   voice=self.voice,
                   progress_callback=self.report_progress,
                   cancel_callback=self.is_cancel_requested,
)

            elif extension == ".pdf":
                output_paths = ConversionPipeline.convert_pdf_to_mp3(
                   input_path=self.input_file,
                   output_dir=self.output_dir,
                   max_words=self.max_words,
                   voice=self.voice,
                   progress_callback=self.report_progress,
                   cancel_callback=self.is_cancel_requested,
)

            else:
                raise ValueError(
                    "Formato não suportado. Use arquivos TXT ou PDF."
                )

            if self._cancel_acknowledged:
               self.cancelled.emit(output_paths)
            else:
               self.finished.emit(output_paths)

        except Exception as exc:
            self.error.emit(str(exc))