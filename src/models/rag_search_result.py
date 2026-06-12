from dataclasses import dataclass

from chromadb.api.types import Metadata

@dataclass
class RAGSearchResult:
    document: str
    distance: float
    metadata: Metadata

    @property
    def similarity(self) -> float:
        '''Convierte la distancia a similitud, asumiendo que la distancia es entre 0 y 1.'''
        return 1 - self.distance 
    
    # Cabe resaltar que ChromaDB ordena los resultados por distancia de "similitud", siendo 0 idéntico 
    # (indistinto del algoritmo de medición de distancia utilizado, gracias ChromeDB por marearme)
    # El método similarity es solo una transformación de la distancia para facilitar su interpretación.