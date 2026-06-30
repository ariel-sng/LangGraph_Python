#!/usr/bin/env -S uv run

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Recibe los nombres de dos archivos por línea de comandos."
    )

    parser.add_argument(
        "file1",
        help="Nombre o ruta del primer archivo.",
    )

    parser.add_argument(
        "file2",
        help="Nombre o ruta del segundo archivo.",
    )

    args = parser.parse_args()

    print(f"Primer archivo: {args.file1}")
    print(f"Segundo archivo: {args.file2}")


if __name__ == "__main__":
    main()