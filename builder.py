import argparse

from migration.seeder.seeder import seed_data
from migration.builder.raw_creation import create_tables


def build_db():
    create_tables()


def seed_db():
    seed_data()


def build():
    build_db()
    seed_db()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database management script.")

    parser.add_argument("-s", "--seed", action="store_true", help="Seed the database")
    parser.add_argument("-b", "--build", action="store_true", help="Build the database")

    args = parser.parse_args()

    if args.build:
        build_db()

    if args.seed:
        seed_db()
