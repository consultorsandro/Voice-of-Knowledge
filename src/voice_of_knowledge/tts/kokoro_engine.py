import torch
from kokoro import KPipeline


class KokoroEngine:
    def __init__(
        self,
        voice: str = "pm_alex",
        lang_code: str = "p",
    ):
        self.voice = voice
        self.lang_code = lang_code
        self.sample_rate = 24000

        self.pipeline = KPipeline(
            lang_code=self.lang_code,
            repo_id="hexgrad/Kokoro-82M",
        )

    def synthesize(self, text: str) -> torch.Tensor:
        if not text.strip():
            raise ValueError("O texto para síntese está vazio")

        generator = self.pipeline(
            text,
            voice=self.voice,
        )

        audio_parts = []

        for _, _, audio in generator:
            audio_parts.append(audio)

        return torch.cat(audio_parts)