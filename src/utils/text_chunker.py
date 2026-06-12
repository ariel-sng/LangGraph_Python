from __future__ import annotations

import re
from typing import List


class TextChunker:
    def __init__(
        self,
        strategy: str = "sentence",    # Sé perfectamente que pude haber hecho un strategy o algo por el estilo, pero con esto basta y estoy quemado
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        valid_strategies = {"fixed", "sentence"}
        if strategy not in valid_strategies:
            raise ValueError(
                f"Unsupported chunking strategy: {strategy}. "
                f"Choose one of {sorted(valid_strategies)}."
            )

        self.strategy = strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        if self.strategy == "fixed":
            return self._split_fixed(text)

        return self._split_sentence(text)

    def _split_fixed(self, text: str) -> List[str]:
        chunks: List[str] = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += max(1, self.chunk_size - self.chunk_overlap)

        return [chunk.strip() for chunk in chunks if chunk.strip()]

    def _split_sentence(self, text: str) -> List[str]:
        sentences = self._split_into_sentences(text)
        chunks: List[str] = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if not current_chunk:
                current_chunk = sentence
                continue

            if len(current_chunk) + 1 + len(sentence) <= self.chunk_size:
                current_chunk = f"{current_chunk} {sentence}"
                continue

            chunks.append(current_chunk.strip())
            current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks or [text.strip()]

    def _split_into_sentences(self, text: str) -> List[str]:
        text = text.replace("\n", " ")
        sentence_end = re.compile(r"(.+?)([.!?…]+(?:\s|$)|$)")

        sentences = [
            (match.group(1) + match.group(2)).strip()
            for match in sentence_end.finditer(text)
            if match.group(1)
        ]

        return sentences
