"""Input-site parsers for extracting initial citation metadata."""

from functools import lru_cache
from importlib import import_module
from pathlib import Path


@lru_cache(maxsize=1)
def load_input_parsers() -> list:
    """Load enabled input parser modules from this directory."""
    parser_dir = Path(__file__).resolve().parent
    parser_modules = []

    for path in sorted(parser_dir.glob("*.py")):
        if path.name == "__init__.py" or path.name.endswith(".disabled.py"):
            continue

        module = import_module(f"{__name__}.{path.stem}")
        parser_modules.append(module)

    parser_modules.sort(key=lambda module: (getattr(module, "PRIORITY", 100), module.__name__))
    return parser_modules
