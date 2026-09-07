import argparse
from pathlib import Path

from voice_of_knowledge.core.conversion_pipeline import ConversionPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Voice of Knowledge - Conversão de TXT/PDF para MP3"
    )

    parser.add_argument(
        "input_file",
        help="Arquivo de entrada (.txt ou .pdf)",
    )

    parser.add_argument(
        "output_dir",
        help="Pasta onde os arquivos MP3 serão salvos",
    )

    parser.add_argument(
        "--max-words",
        type=int,
        default=350,
        help="Quantidade aproximada máxima de palavras por parte",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    input_path = Path(args.input_file)
    output_dir = Path(args.output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    extension = input_path.suffix.lower()

    if extension == ".txt":
        output_paths = ConversionPipeline.convert_txt_to_mp3(
            str(input_path),
            str(output_dir),
            args.max_words,
        )

    elif extension == ".pdf":
        output_paths = ConversionPipeline.convert_pdf_to_mp3(
            str(input_path),
            str(output_dir),
            args.max_words,
        )

    else:
        raise ValueError(
            "Formato não suportado. Use arquivos .txt ou .pdf."
        )

    print()
    print("Conversão concluída.")
    print(f"Arquivos gerados: {len(output_paths)}")

    for path in output_paths:
        print(path)


if __name__ == "__main__":
    main()