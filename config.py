"""Configurazione base per l'ambiente di sviluppo AssoHUB."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from django.core.management.utils import get_random_secret_key


@dataclass
class Settings:
    base_dir: Path = Path(__file__).resolve().parent
    db_name: str = str(base_dir / "db.sqlite3")
    secret_key: str = get_random_secret_key()


def load_settings() -> Settings:
    """Restituisce le impostazioni di base per inizializzare l'applicazione."""

    return Settings()

