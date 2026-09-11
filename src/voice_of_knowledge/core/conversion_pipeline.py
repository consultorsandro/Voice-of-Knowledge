from collections.abc import Callable
from pathlib import Path

from voice_of_knowledge.export.audio_exporter import AudioExporter
from voice_of_knowledge.loaders.pdf_loader import PdfLoader
from voice_of_knowledge.loaders.text_loader import TextLoader
from voice_of_knowledge.segmentation.text_segmenter import TextSegmenter
from voice_of_knowledge.tts.kokoro_engine import KokoroEngine


class ConversionPipeline:
    @staticmethod
    def prepare_text(
        input_path: str,
        max_words: int,
    ) -> list[str]:
        text = TextLoader.load(input_path)

        chunks = TextSegmenter.split(
            text,
            max_words,
        )

        return chunks

    @staticmethod
    def prepare_pdf(
        input_path: str,
        max_words: int,
    ) -> list[str]:
        text = PdfLoader.load(input_path)

        chunks = TextSegmenter.split(
            text,
            max_words,
        )

        return chunks

    @staticmethod
    def convert_txt_to_mp3(
        input_path: str,
        output_dir: str,
        max_words: int = 350,
        voice: str = "pm_alex",
        progress_callback: Callable[[int, int, int], None] | None = None,
        cancel_callback: Callable[[], bool] | None = None,
    ) -> list[Path]:
        chunks = ConversionPipeline.prepare_text(
            input_path,
            max_words,
        )

        engine = KokoroEngine(voice=voice)
        output_paths = []


        for index, chunk in enumerate(chunks, start=1):
            if cancel_callback is not None and cancel_callback():
                print("Conversão cancelada.")
                break

            output_path = Path(output_dir) / f"parte_{index:03d}.mp3"

            if output_path.exists():
                print(
                    f"Parte {index}/{len(chunks)} já existe. Pulando..."
                )
                output_paths.append(output_path)
                continue

            if progress_callback is not None:
                progress_callback(
                    index,
                    len(chunks),
                    len(chunk.split()),
                )

            print(
                f"Gerando parte {index}/{len(chunks)} "
                f"({len(chunk.split())} palavras)..."
            )

            audio = engine.synthesize(chunk)

            AudioExporter.save_mp3(
                audio,
                engine.sample_rate,
                str(output_path),
            )

            output_paths.append(output_path)

        return output_paths

    @staticmethod
    def convert_pdf_to_mp3(
        input_path: str,
        output_dir: str,
        max_words: int = 350,
        voice: str = "pm_alex",
        progress_callback: Callable[[int, int, int], None] | None = None,
        cancel_callback: Callable[[], bool] | None = None,
    ) -> list[Path]:
        chunks = ConversionPipeline.prepare_pdf(
            input_path,
            max_words,
        )

        engine = KokoroEngine(voice=voice)
        output_paths = []

        for index, chunk in enumerate(chunks, start=1):
            if cancel_callback is not None and cancel_callback():
                print("Conversão cancelada.")
                break

            output_path = Path(output_dir) / f"parte_{index:03d}.mp3"
          
            if output_path.exists():
                print(
                    f"Parte {index}/{len(chunks)} já existe. Pulando..."
                )
                output_paths.append(output_path)
                continue

            if progress_callback is not None:
                progress_callback(
                    index,
                    len(chunks),
                    len(chunk.split()),
                )

            print(
                f"Gerando parte {index}/{len(chunks)} "
                f"({len(chunk.split())} palavras)..."
            )

            audio = engine.synthesize(chunk)

            AudioExporter.save_mp3(
                audio,
                engine.sample_rate,
                str(output_path),
            )

            output_paths.append(output_path)

        return output_paths