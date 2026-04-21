import os
import sys
import traceback
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
os.chdir(PROJECT_ROOT)

os.environ.setdefault("APP_NAME", "Nutrition and Recipe Analytics API")
os.environ.setdefault("API_KEY", "dev-secret-key")
os.environ.setdefault("DATABASE_URL", f"sqlite:///{PROJECT_ROOT / 'nutrition.db'}")

LOG_PATH = PROJECT_ROOT / "pythonanywhere_boot.log"


def write_boot_log(message: str) -> None:
    LOG_PATH.write_text(message, encoding="utf-8")


if __name__ == "__main__":
    try:
        from uvicorn import main

        sys.argv = [
            "uvicorn",
            "app.main:app",
            "--app-dir",
            str(PROJECT_ROOT),
            "--uds",
            os.environ["DOMAIN_SOCKET"],
        ]
        main()
    except Exception:
        write_boot_log(traceback.format_exc())
        raise
