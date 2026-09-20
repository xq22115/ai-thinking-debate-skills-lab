"""Import shim for the hyphenated control-plane directory used by repository tooling."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

_path = Path(__file__).resolve().parent / "control-plane" / "autonomy" / "engine.py"
_spec = spec_from_file_location("autonomy_engine", _path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"cannot load {_path}")
engine = module_from_spec(_spec)
_spec.loader.exec_module(engine)
