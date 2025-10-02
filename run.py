"""Punto di ingresso per avviare l'applicazione AssoHUB."""
from __future__ import annotations

import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "assohub.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line([sys.argv[0], "runserver", "0.0.0.0:8000"])


if __name__ == "__main__":
    main()
