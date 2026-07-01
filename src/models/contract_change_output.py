from pydantic import BaseModel, Field


class ContractChangeOutput(BaseModel):
    sections_changed: list[str] = Field(
        description=(
            "Lista de las secciones del contrato que fueron modificadas, "
            "agregadas o eliminadas por la enmienda. Utilizá los nombres "
            "o identificadores de las secciones cuando estén disponibles."
        )
    )

    topics_touched: list[str] = Field(
        description=(
            "Lista de las categorías legales o comerciales afectadas por los cambios, "
            "por ejemplo: Plazo, Pago, Confidencialidad, Terminación, "
            "Responsabilidades, Propiedad Intelectual, entre otras."
        )
    )

    summary_of_the_change: str = Field(
        description=(
            "Descripción clara y detallada de todos los cambios introducidos por la enmienda. "
            "Debe explicar qué se agregó, qué se eliminó y qué se modificó, "
            "sin omitir cambios relevantes."
        )
    )