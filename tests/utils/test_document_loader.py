import pytest
import tempfile
from pathlib import Path
from src.utils.document_loader import DocumentLoader


class TestDocumentLoader:
    """Tests básicos para DocumentLoader"""

    @pytest.fixture
    def loader(self):
        """Fixture que proporciona una instancia de DocumentLoader"""
        return DocumentLoader()

    @pytest.fixture
    def temp_file(self):
        """Fixture que crea un archivo temporal con contenido"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write("Este es un documento de prueba.\nCon múltiples líneas.")
            temp_path = f.name
        yield temp_path
        # Limpieza
        Path(temp_path).unlink()

    def test_load_existing_file(self, loader, temp_file):
        """Test que verifica que se puede cargar un archivo existente"""
        content = loader.load(temp_file)
        assert content == "Este es un documento de prueba.\nCon múltiples líneas."

    def test_load_returns_string(self, loader, temp_file):
        """Test que verifica que el contenido cargado es un string"""
        content = loader.load(temp_file)
        assert isinstance(content, str)

    def test_load_non_existing_file(self, loader):
        """Test que verifica que se lanza FileNotFoundError para archivo inexistente"""
        with pytest.raises(FileNotFoundError) as exc_info:
            loader.load("/ruta/que/no/existe/archivo.txt")
        assert "Document not found" in str(exc_info.value)

    def test_load_preserves_formatting(self, loader):
        """Test que verifica que se preserva el formato del documento"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            test_content = "Línea 1\n\nLínea 3 con espacios:   espacios"
            f.write(test_content)
            temp_path = f.name
        
        try:
            content = loader.load(temp_path)
            assert content == test_content
        finally:
            Path(temp_path).unlink()

    def test_load_empty_file(self, loader):
        """Test que verifica que se puede cargar un archivo vacío"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_path = f.name
        
        try:
            content = loader.load(temp_path)
            assert content == ""
            assert isinstance(content, str)
        finally:
            Path(temp_path).unlink()

    def test_load_special_characters(self, loader):
        """Test que verifica la carga de caracteres especiales"""
        special_content = "Acentos: áéíóú\nCaracteres especiales: ñ, @, #, $\nEmojis: 😀"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write(special_content)
            temp_path = f.name
        
        try:
            content = loader.load(temp_path)
            assert content == special_content
        finally:
            Path(temp_path).unlink()
