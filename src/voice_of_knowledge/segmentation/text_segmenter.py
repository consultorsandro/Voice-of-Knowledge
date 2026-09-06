import re


class TextSegmenter:
    @staticmethod
    def split(text: str, max_words: int) -> list[str]:
        if max_words <= 0:
            raise ValueError("max_words deve ser maior que zero")

        if not text.strip():
            return []

        sentences = re.split(r"(?<=[.!?])\s+", text.strip())

        chunks = []
        current_chunk = []
        current_word_count = 0

        for sentence in sentences:
            sentence_word_count = len(sentence.split())

            if current_chunk and current_word_count + sentence_word_count > max_words:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_word_count = 0

            current_chunk.append(sentence)
            current_word_count += sentence_word_count

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks