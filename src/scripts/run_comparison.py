from pathlib import Path
import argparse

from src.utils.graph_builder import build_img_graph
from src.utils.prints import *

from src.observability.langfuse import *

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("file1")
    parser.add_argument("file2")

    args = parser.parse_args()

    # Paso 1: Carga los archivos
    
    file1, file2 = get_file_names(parser, args)

    # Paso 2: Construye el grafo
    
    print_header("CREANDO GRAFO...")
    
    graph = build_img_graph()
    
    print_success("Grafo finalizado correctamente")
    
    # Paso 3: 
    print_header("Ejecutando al Agente Autónomo de Comparación de Contratos...")
    
    with langfuse.start_as_current_observation(
        as_type="span",
        name="contract-analysis",
    ):
        result = graph.invoke(
            {
                "contract_image_path": file1,
                "amendment_image_path": file2,
                "contract_text": "",
                "amendment_text": "",
                "contract_context": "",
                "amendment_context": "",
                "validated_output": None,
            },
            config={
                "callbacks": [langfuse_handler]
            }
        )

    print_success("Agente ejecutado correctamente")

    final_result = result["validated_output"] 

    print_contract_change_output(final_result)

def get_file_names(parser, args):
    base_dir = Path("contracts")

    file1 = base_dir / args.file1
    file2 = base_dir / args.file2

    missing = [
        str(path)
        for path in (file1, file2)
        if not path.is_file()
    ]
    if missing:
        parser.error("El/los siguiente(s) archivo(s) no existen:\n" + "\n".join(missing))

    print(f" Primer archivo cargado exitosamente:\t '{args.file1}'")
    print(f"Segundo archivo cargado exitosamente:\t '{args.file2}'")

    return file1,file2

if __name__ == "__main__":
    main()