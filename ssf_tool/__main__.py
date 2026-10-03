"""CLI entrypoint for ssf_tool."""

import sys
from .seed import run_seed


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] == "--help" or args[0] == "-h":
        print("Uso: python -m ssf_tool <comando>")
        print("\nComandos disponibles:")
        print("  seed       Siembra categorías, productos de demostración y ventas mediante la API")
        sys.exit(0)

    command = args[0]
    if command == "seed":
        run_seed()
    else:
        print(f"Error: comando desconocido '{command}'. Ejecute --help para ayuda.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
