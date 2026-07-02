from pathlib import Path
import argparse
import sys
import time

from openai import APIConnectionError, APIError, APITimeoutError, BadRequestError, OpenAIError, RateLimitError

from src.config.settings import Settings
from src.utils.graph_builder import build_img_graph
from src.utils.prints import *

from src.observability.langfuse import *


def invoke_graph_with_retries(graph, payload, callbacks):
    max_attempts = Settings.OPENAI_API_RETRY_ATTEMPTS

    for attempt in range(1, max_attempts + 1):
        try:
            return graph.invoke(
                payload,
                config={"callbacks": callbacks},
            )

        # Si caigo a un error recuperable...
        except (RateLimitError, APITimeoutError, APIConnectionError, APIError) as exc:
            # ... me fijo si usé todos los intentos, y si es el caso levanto un error....
            if attempt == max_attempts:
                raise RuntimeError(
                    "Error de API de OpenAI después de varios intentos. Revisa la conexión y vuelve a intentar."
                ) from exc

            # ... Si no prosigo con normalidad, agregando delay y se reduce en uno mis intentos
            delay = Settings.OPENAI_API_RETRY_BACKOFF * attempt
            print(f"Reintentando operación de OpenAI ({attempt}/{max_attempts}) en {delay:.0f}s...")
            time.sleep(delay)

        except OpenAIError as exc:
            raise RuntimeError("Error de OpenAI no recuperable.") from exc

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
    
    # Paso 3:  Ejecuto el grafo
    print_header("Ejecutando al Agente Autónomo de Comparación de Contratos...")
    
    try:
        # Agrego trazabilidad con un span en la raíz del grafo
        with langfuse.start_as_current_observation(
            as_type="span",
            name="contract-analysis",
        ) as root_span:
            
            root_span.update(
                input={
                    "contract_image_path": file1,
                    "amendment_image_path": file2,
                }
            )

            try:
                result = invoke_graph_with_retries(
                    graph,
                    {
                        "contract_image_path": file1,
                        "amendment_image_path": file2,
                        "contract_text": "",
                        "amendment_text": "",
                        "contract_context": "",
                        "amendment_context": "",
                        "validated_output": None,
                    },
                    [langfuse_handler],
                )
            except Exception as exc:
                err = str(exc)
                print_error(f"Error en el grafo: {err}")
                root_span.update(
                    output={
                        "status": "error",
                        "step": "invoke_graph_with_retries",
                        "message": err,
                    }
                )
                raise

            validated_output = result["validated_output"]
            serialized_output = validated_output.model_dump()

            root_span.update(output=serialized_output)

    except Exception as exc:
        print_error(f"Error inesperado: {exc}")
        sys.exit(1)
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