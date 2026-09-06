from kokoro import KPipeline
import soundfile as sf
import numpy as np

TEXT = """
Olá. Este é o primeiro teste do projeto Voice of Knowledge.

Nosso objetivo é transformar textos, artigos e livros em arquivos de áudio
para facilitar e acelerar o estudo.

Se você está ouvindo esta mensagem com clareza, nosso primeiro teste
de síntese de voz em português brasileiro funcionou.
"""

pipeline = KPipeline(lang_code="p")


def gerar_audio(nome_arquivo: str, voz: str):
    print(f"Gerando voz: {voz}")

    generator = pipeline(
        TEXT,
        voice=voz,
        speed=1.0
    )

    audio_chunks = []

    for result in generator:
        if result.audio is not None:
            audio_chunks.append(result.audio.numpy())

    if not audio_chunks:
        raise RuntimeError(f"Nenhum áudio foi gerado para a voz {voz}")

    audio_completo = np.concatenate(audio_chunks)

    sf.write(
        nome_arquivo,
        audio_completo,
        24000
    )

    print(f"Arquivo criado: {nome_arquivo}")


gerar_audio("voz_feminina_dora.wav", "pf_dora")
gerar_audio("voz_masculina_alex.wav", "pm_alex")

print("Teste concluído.")