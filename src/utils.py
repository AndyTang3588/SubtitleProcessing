from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Tuple

_POSITION_PATTERN = re.compile(r"^output([a-zA-Z]?)(\d+)$")
_LETTER_PRIORITY = {"a": 1, "b": 2, "c": 3}


def _position_to_rank(position: str) -> Tuple[int, int]:
    """
    Convert a logical script position (e.g. "a2") to a sortable rank tuple.
    Larger tuples represent later scripts according to the custom order.
    """
    normalized = position.strip().lower()
    if not normalized:
        raise ValueError("Position string cannot be empty.")

    if normalized[0].isalpha():
        letter = normalized[0]
        digits = normalized[1:]
    else:
        letter = ""
        digits = normalized

    if not digits or not digits.isdigit():
        raise ValueError(f"Unable to parse numeric part from position '{position}'.")

    letter_rank = _LETTER_PRIORITY.get(letter, 0)
    number_rank = int(digits)
    return letter_rank, number_rank


def get_previous_output_file(
    current_position: str, cache_dir: str | Path = "cache"
) -> Optional[str]:
    """
    Return the path of the output file produced by the script that runs immediately
    before the current script according to the custom order (c > b > a and 3 > 2 > 1).

    Args:
        current_position: The logical position string of the current script (e.g. "a3").
        cache_dir: Directory that stores output files (defaults to "cache").

    Returns:
        The file path (as a string) of the previous script's output, or None if there is
        no previous output.
    """
    cache_path = Path(cache_dir)
    if not cache_path.exists():
        raise FileNotFoundError(f"Cache directory '{cache_dir}' does not exist.")

    current_rank = _position_to_rank(current_position)
    ranked_files: list[tuple[Tuple[int, int], Path]] = []

    for file_path in cache_path.iterdir():
        if not file_path.is_file():
            continue
        match = _POSITION_PATTERN.match(file_path.stem)
        if not match:
            continue
        letter, number = match.groups()
        letter_rank = _LETTER_PRIORITY.get(letter.lower(), 0)
        number_rank = int(number)
        ranked_files.append(((letter_rank, number_rank), file_path))

    ranked_files.sort(key=lambda item: (item[0][0], item[0][1], item[1].suffix, item[1].name))

    previous_path: Optional[Path] = None
    for rank, file_path in ranked_files:
        if rank < current_rank:
            previous_path = file_path
        else:
            break

    return str(previous_path) if previous_path else None
