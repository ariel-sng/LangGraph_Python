import json
from datetime import datetime, timezone
from pathlib import Path


def append_jsonl_record(
    record: dict,
    storage_dir: Path = Path("storage") / "PI4",
    filename: str = "pi4_results.jsonl",
) -> Path:
    """Append a single JSONL record to a persistent PI4 file.

    Each record is written as one JSON object per line, and the storage
    directory is created if it does not exist.
    """
    storage_dir.mkdir(parents=True, exist_ok=True)
    output_file = storage_dir / filename

    record_with_meta = {
        "saved_at": datetime.now(timezone.utc).isoformat(),
        **record,
    }

    with output_file.open("a", encoding="utf-8") as handle:
        json.dump(record_with_meta, handle, ensure_ascii=False)
        handle.write("\n")

    return output_file
