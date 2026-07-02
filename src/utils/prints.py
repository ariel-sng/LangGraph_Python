from src.models.contract_change_output import ContractChangeOutput

import shutil
import textwrap

def print_header(title: str) -> None:
    width = 66

    print(f"┌{'─' * width}┐")
    print(f"│ ⚙ {title:<{width - 3}}│")
    print(f"└{'─' * width}┘")


def print_success(message: str = "Proceso finalizado correctamente.") -> None:
    width = 66

    print(f"┌{'─' * width}┐")
    print(f"│ ☑ {message:<{width - 3}}│")
    print(f"└{'─' * width}┘")

def print_error(message: str = "Se produjo un error.") -> None:
    terminal_width = shutil.get_terminal_size(fallback=(80, 20)).columns

    prefix = "⚠ "
    max_content = terminal_width - 4  # │ + espacio + espacio + │

    lines = textwrap.wrap(
        prefix + message,
        width=max_content,
        break_long_words=True
    )

    width = max(len(line) for line in lines)

    print(f"┌{'─' * (width + 2)}┐")
    for line in lines:
        print(f"│ {line:<{width}} │")
    print(f"└{'─' * (width + 2)}┘")    



def print_contract_change_output(output: ContractChangeOutput) -> None:
    print("=" * 35)
    print("")
    print("=" * 35)


    print("\nSecciones modificadas:")
    if output.sections_changed:
        for section in output.sections_changed:
            print(f"  • {section}")
    else:
        print("  Ninguna")

    print("\nTemas afectados:")
    if output.topics_touched:
        for topic in output.topics_touched:
            print(f"  • {topic}")
    else:
        print("  Ninguno")

    print("\nResumen de los cambios:")
    print(output.summary_of_the_change)

    print("\n" + "=" * 60)
