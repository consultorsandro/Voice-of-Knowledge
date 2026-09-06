from pathlib import Path
import re
import time

import lameenc
import numpy as np
from kokoro import KPipeline


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "samples" / "teste.txt"
OUTPUT_DIR = BASE_DIR / "output" / "teste_mp3"

VOICE = "pm_alex"
LANG_CODE = "p"
SPEED = 1.0
SAMPLE_RATE = 24000

# Aproximação inicial para ~2 min 30 s.
TARGET_WORDS_PER_PART = 380


def carregar_texto(caminho: Path) -> str:
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    texto = caminho.read_text(encoding="utf-8").strip()

    if not texto:
        raise ValueError("O arquivo está vazio.")

    return texto


def dividir_em_sentencas(texto: str) -> list[str]:
    return [
        sentenca.strip()
        for sentenca in re.split(r"(?<=[.!?])\s+", texto)
        if sentenca.strip()
    ]


def dividir_texto(texto: str, limite_palavras: int) -> list[str]:
    sentencas = dividir_em_sentencas(texto)

    partes = []
    parte_atual = []
    palavras_atuais = 0

    for sentenca in sentencas:
        quantidade = len(sentenca.split())

        if parte_atual and palavras_atuais + quantidade > limite_palavras:
            partes.append(" ".join(parte_atual))
            parte_atual = []
            palavras_atuais = 0

        parte_atual.append(sentenca)
        palavras_atuais += quantidade

    if parte_atual:
        partes.append(" ".join(parte_atual))

    return partes


def gerar_audio(pipeline: KPipeline, texto: str) -> np.ndarray:
    generator = pipeline(
        texto,
        voice=VOICE,
        speed=SPEED
    )

    blocos = []

    for resultado in generator:
        if resultado.audio is not None:
            blocos.append(resultado.audio.numpy())

    if not blocos:
        raise RuntimeError("Nenhum áudio foi gerado.")

    return np.concatenate(blocos)


def salvar_mp3(audio: np.ndarray, arquivo_saida: Path):
    audio = np.clip(audio, -1.0, 1.0)

    pcm = (audio * 32767).astype(np.int16)

    encoder = lameenc.Encoder()
    encoder.set_bit_rate(96)
    encoder.set_in_sample_rate(SAMPLE_RATE)
    encoder.set_channels(1)
    encoder.set_quality(2)

    mp3_data = encoder.encode(pcm.tobytes())
    mp3_data += encoder.flush()

    arquivo_saida.write_bytes(mp3_data)


def main():
    print("Voice of Knowledge")
    print("------------------")

    texto = carregar_texto(INPUT_FILE)
    partes = dividir_texto(texto, TARGET_WORDS_PER_PART)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pipeline = KPipeline(
        lang_code=LANG_CODE,
        repo_id="hexgrad/Kokoro-82M"
    )

    inicio_total = time.perf_counter()

    duracao_audio_total = 0.0

    print(f"Partes: {len(partes)}")
    print()

    for indice, parte in enumerate(partes, start=1):
        inicio_parte = time.perf_counter()

        arquivo_saida = OUTPUT_DIR / f"parte_{indice:03d}.mp3"

        print(
            f"Gerando parte {indice}/{len(partes)} "
            f"({len(parte.split())} palavras)..."
        )

        audio = gerar_audio(pipeline, parte)

        duracao_audio = len(audio) / SAMPLE_RATE
        duracao_audio_total += duracao_audio

        salvar_mp3(audio, arquivo_saida)

        tempo_processamento = time.perf_counter() - inicio_parte

        print(
            f"OK: {arquivo_saida.name} | "
            f"áudio: {duracao_audio / 60:.2f} min | "
            f"processamento: {tempo_processamento:.2f} s"
        )

    tempo_total = time.perf_counter() - inicio_total

    print()
    print("Processamento concluído.")
    print(f"Áudio total: {duracao_audio_total / 60:.2f} min")
    print(f"Tempo total de geração: {tempo_total / 60:.2f} min")

    if tempo_total > 0:
        fator = duracao_audio_total / tempo_total
        print(f"Velocidade aproximada: {fator:.2f}x tempo real")


if __name__ == "__main__":
    main()