from dotenv import load_dotenv

load_dotenv()
from src.adapters.driven.infra.migration.raw_creation import create_tables


def build_db():
    create_tables()


def seed_db():
    pass


def build():
    build_db()
    seed_db()


if __name__ == "__main__":
    build()
