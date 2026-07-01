from pathlib import Path
import argparse

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

    print(f"Primer archivo: {args.file1}")
    print(f"Segundo archivo: {args.file2}")

if __name__ == "__main__":
    main()