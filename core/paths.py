from pathlib import Path
import os, sys

def app_root() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[1]

def user_data_dir() -> Path:
    base = Path(os.environ.get("APPDATA") or (Path.home() / "AppData" / "Roaming"))
    path = base / "LuminaPlayer"
    path.mkdir(parents=True, exist_ok=True)
    return path
