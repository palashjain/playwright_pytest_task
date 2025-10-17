from datetime import datetime
from pathlib import Path


def generate_polygon_name(prefix: str) -> str:
    return f"{prefix}_{generate_timestamp()}"


def generate_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def validate_downloaded_file(file_path: Path) -> None:
    if not file_path.exists():
        raise AssertionError(f"Downloaded file not found at: {file_path}")

    if file_path.stat().st_size == 0:
        raise AssertionError(f"Downloaded file is empty: {file_path}")


def generate_unique_filename(original_filename: str) -> str:
    name_part, ext_part = original_filename.rsplit('.', 1) if '.' in original_filename else (original_filename, '')
    timestamp = generate_timestamp()
    return f"{name_part}_{timestamp}.{ext_part}" if ext_part else f"{name_part}_{timestamp}"
