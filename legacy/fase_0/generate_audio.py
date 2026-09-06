from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "samples" / "teste.txt"
OUTPUT_DIR = BASE_DIR / "output"

VOICE = "pm_alex"
LANG_CODE = "p"
SPEED = 1.0
SAMPLE_RATE = 24000


def carregar_texto(caminho: Path) -> str:
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    texto = caminho.read_text(encoding="utf-8").strip()

    if not texto:
        raise ValueError("O arquivo de texto está vazio.")

    return texto


def gerar_audio(texto: str, arquivo_saida: Path):
    pipeline = KPipeline(lang_code=LANG_CODE)

    generator = pipeline(
        texto,
        voice=VOICE,
        speed=SPEED
    )

    blocos_audio = []

    for resultado in generator:
        if resultado.audio is not None:
            blocos_audio.append(resultado.audio.numpy())

    if not blocos_audio:
        raise RuntimeError("O Kokoro não gerou nenhum áudio.")

    audio_completo = np.concatenate(blocos_audio)

    sf.write(
        arquivo_saida,
        audio_completo,
        SAMPLE_RATE
    )


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Voice of Knowledge")
    print("------------------")
    print(f"Entrada: {INPUT_FILE.name}")
    print(f"Voz: {VOICE}")

    texto = carregar_texto(INPUT_FILE)

    arquivo_saida = OUTPUT_DIR / f"{INPUT_FILE.stem}_{VOICE}.wav"

    print("Gerando áudio...")

    gerar_audio(texto, arquivo_saida)

    print("Concluído.")
    print(f"Arquivo criado em: {arquivo_saida}")


if __name__ == "__main__":
    main()