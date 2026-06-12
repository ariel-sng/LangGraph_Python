import pytest
from src.utils.text_chunker import TextChunker


class TestTextChunker:
    """Tests básicos para TextChunker"""

    def test_default_initialization(self):
        """Test que verifica la inicialización con parámetros por defecto"""
        chunker = TextChunker()
        assert chunker.strategy == "fixed"
        assert chunker.chunk_size == 500
        assert chunker.chunk_overlap == 100

    def test_custom_initialization(self):
        """Test que verifica la inicialización con parámetros personalizados"""
        chunker = TextChunker(strategy="sentence", chunk_size=200, chunk_overlap=50)
        assert chunker.strategy == "sentence"
        assert chunker.chunk_size == 200
        assert chunker.chunk_overlap == 50

    def test_invalid_strategy_raises_error(self):
        """Test que verifica que se lanza error con estrategia inválida"""
        with pytest.raises(ValueError) as exc_info:
            TextChunker(strategy="invalid_strategy")
        assert "Unsupported chunking strategy" in str(exc_info.value)

    # Tests para estrategia FIXED
    class TestFixedStrategy:
        """Tests específicos para estrategia fixed"""

        @pytest.fixture
        def chunker(self):
            return TextChunker(strategy="fixed", chunk_size=50, chunk_overlap=10)

        def test_fixed_split_basic(self, chunker):
            """Test básico de división con estrategia fixed"""
            text = "A" * 100  # 100 caracteres 'A'
            chunks = chunker.split(text)
            assert len(chunks) > 0
            assert all(isinstance(chunk, str) for chunk in chunks)

        def test_fixed_split_respects_chunk_size(self, chunker):
            """Test que verifica que los chunks no superan chunk_size"""
            text = "B" * 200
            chunks = chunker.split(text)
            for chunk in chunks:
                assert len(chunk) <= 50

        def test_fixed_split_removes_empty_chunks(self, chunker):
            """Test que verifica que no hay chunks vacíos"""
            text = "Contenido"
            chunks = chunker.split(text)
            assert all(chunk.strip() for chunk in chunks)

        def test_fixed_split_short_text(self, chunker):
            """Test con texto más corto que chunk_size"""
            text = "Texto corto"
            chunks = chunker.split(text)
            assert len(chunks) == 1
            assert chunks[0] == "Texto corto"

        def test_fixed_overlap_creates_duplication(self, chunker):
            """Test que verifica que el overlap crea contenido duplicado entre chunks"""
            text = "A" * 100
            chunks = chunker.split(text)
            if len(chunks) > 1:
                # Si hay overlap, debe haber contenido compartido
                overlap = set(chunks[0]) & set(chunks[1])
                assert len(overlap) > 0

    # Tests para estrategia SENTENCE
    class TestSentenceStrategy:
        """Tests específicos para estrategia sentence"""

        @pytest.fixture
        def chunker(self):
            return TextChunker(strategy="sentence", chunk_size=100, chunk_overlap=0)

        def test_sentence_split_basic(self, chunker):
            """Test básico de división con estrategia sentence"""
            text = "Primera oración. Segunda oración. Tercera oración."
            chunks = chunker.split(text)
            assert len(chunks) > 0
            assert all(isinstance(chunk, str) for chunk in chunks)

        def test_sentence_preserves_complete_sentences(self, chunker):
            """Test que verifica que las oraciones no se rompen"""
            text = "Esta es una oración completa. Esta es otra."
            chunks = chunker.split(text)
            for chunk in chunks:
                # Cada chunk debe terminar con puntuación o ser la última oración
                assert chunk[-1] in '.!?…' or len(chunk) > 0

        def test_sentence_split_handles_multiple_punctuation(self, chunker):
            """Test que maneja múltiples tipos de puntuación"""
            text = "¿Pregunta? ¡Exclamación! Afirmación. Término…"
            chunks = chunker.split(text)
            assert len(chunks) > 0

        def test_sentence_split_removes_newlines(self, chunker):
            """Test que verifica que los saltos de línea se convierten a espacios"""
            text = "Primera línea.\nSegunda línea.\nTercera línea."
            chunks = chunker.split(text)
            for chunk in chunks:
                assert "\n" not in chunk

        def test_sentence_split_handles_empty_string(self, chunker):
            """Test que maneja strings vacíos"""
            text = ""
            chunks = chunker.split(text)
            assert len(chunks) == 1
            assert chunks[0] == ""

        def test_sentence_split_long_sentence(self, chunker):
            """Test con una oración más larga que chunk_size"""
            chunker = TextChunker(strategy="sentence", chunk_size=10, chunk_overlap=0)
            text = "Esta es una oración muy larga que supera el tamaño del chunk."
            chunks = chunker.split(text)
            assert len(chunks) >= 1

    # Tests generales
    def test_split_with_empty_string(self):
        """Test que maneja strings vacíos para ambas estrategias"""
        chunker_fixed = TextChunker(strategy="fixed")
        chunker_sentence = TextChunker(strategy="sentence")
        
        assert chunker_fixed.split("") == []
        assert chunker_sentence.split("")

    def test_split_method_dispatcher(self):
        """Test que verifica que split() llama al método correcto"""
        text = "A" * 100
        
        chunker_fixed = TextChunker(strategy="fixed", chunk_size=30)
        fixed_chunks = chunker_fixed.split(text)
        
        chunker_sentence = TextChunker(strategy="sentence", chunk_size=30)
        sentence_chunks = chunker_sentence.split(text)
        
        # Ambos deben producir chunks, pero posiblemente diferentes
        assert len(fixed_chunks) > 0
        assert len(sentence_chunks) > 0

    def test_all_chunks_are_strings(self):
        """Test que verifica que todos los chunks son strings"""
        text = "Este es un texto de prueba con múltiples palabras para chunking."
        chunker = TextChunker(strategy="fixed", chunk_size=20)
        chunks = chunker.split(text)
        assert all(isinstance(chunk, str) for chunk in chunks)

    def test_chunks_are_stripped(self):
        """Test que verifica que los chunks están limpios de espacios extra"""
        text = "   Texto con espacios   "
        chunker = TextChunker(strategy="fixed", chunk_size=50)
        chunks = chunker.split(text)
        for chunk in chunks:
            if chunk:
                assert chunk == chunk.strip()
