from src.models.contract_change_output import ContractChangeOutput


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
