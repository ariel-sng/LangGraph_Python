from pathlib import Path
import argparse

from src.utils.graph_builder import build_img_chain

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("file1")
    parser.add_argument("file2")

    args = parser.parse_args()

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

    chain = build_img_chain()

    result = chain.invoke(
        {
            "contract_image_path": file1,
            "amendment_image_path": file2,
            "contract_text": "",
            "amendment_text": "",
            "contextual_map": "",
        }
    )

    print("##### PRIMER  CONTRATO #####")
    
    print(result["contract_text"])
    
    
    print("##### SEGUNDO CONTRATO #####")

    print(result["amendment_text"])

if __name__ == "__main__":
    main()