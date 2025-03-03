from dotenv import load_dotenv
import os

load_dotenv()

TURSO_URL = os.getenv("TURSO_DATABASE_URL")
TURSO_AUTH = os.getenv("TURSO_AUTH_TOKEN")
