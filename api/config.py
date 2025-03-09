from dotenv import load_dotenv
import os

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M",
        },
        "simple": {"format": "[%(levelname)s] %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "detailed",
            "filename": "app.log",
            "mode": "a",
        },
    },
    "root": {"level": "WARNING", "handlers": ["console", "file"]},
}

load_dotenv()

TURSO_URL = os.getenv("TURSO_DATABASE_URL")
TURSO_AUTH = os.getenv("TURSO_AUTH_TOKEN")
