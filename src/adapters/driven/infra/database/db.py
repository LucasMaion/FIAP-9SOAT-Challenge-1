import os
from peewee import PostgresqlDatabase

# Configure the PostgreSQL database
db = PostgresqlDatabase(
    os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
)


def start_db():
    db.connect()


def close_db():
    db.close()
