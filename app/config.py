import os

from dotenv import load_dotenv

load_dotenv()

# Application settings
APP_NAME = os.getenv("APP_NAME", "joefg-bot")
TG_TOKEN = os.getenv("TG_TOKEN")

# Debug settings
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Datastore settings
DB_PATH = os.getenv("DB_PATH", "database/database.sqlite3")

# Developer chat
DEV_CHAT = os.getenv("DEV_CHAT")
