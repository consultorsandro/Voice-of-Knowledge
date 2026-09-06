from pathlib import Path
import subprocess
import tempfile

import imageio_ffmpeg
import soundfile as sf
import torch


class AudioExporter:
    @staticmethod
    def _validate_audio(audio: torch.Tensor) -> None:
        if audio.numel() == 0:
            raise ValueError("O áudio está vazio")

    @staticmethod
    def _validate_sample_rate(sample_rate: int) -> None:
        if sample_rate <= 0:
            raise ValueError("sample_rate deve ser maior que zero")

    @staticmethod
    def _validate_output_path(output_path: str) -> None:
        if not output_path.strip():
            raise ValueError("O caminho de saída está vazio")

    @staticmethod
    def save_wav(
        audio: torch.Tensor,
        sample_rate: int,
        output_path: str,
    ) -> None:
        AudioExporter._validate_audio(audio)
        AudioExporter._validate_sample_rate(sample_rate)
        AudioExporter._validate_output_path(output_path)

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        audio_numpy = audio.detach().cpu().numpy()

        sf.write(
            path,
            audio_numpy,
            sample_rate,
        )

    @staticmethod
    def save_mp3(
        audio: torch.Tensor,
        sample_rate: int,
        output_path: str,
    ) -> None:
        AudioExporter._validate_audio(audio)
        AudioExporter._validate_sample_rate(sample_rate)
        AudioExporter._validate_output_path(output_path)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_wav = Path(temp_file.name)

        try:
            AudioExporter.save_wav(
                audio,
                sample_rate,
                str(temp_wav),
            )

            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

            subprocess.run(
                [
                    ffmpeg_exe,
                    "-y",
                    "-i",
                    str(temp_wav),
                    "-codec:a",
                    "libmp3lame",
                    "-q:a",
                    "2",
                    str(output),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        finally:
            if temp_wav.exists():
                temp_wav.unlink()