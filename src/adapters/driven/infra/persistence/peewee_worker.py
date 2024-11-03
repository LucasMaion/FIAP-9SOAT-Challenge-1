from loguru import logger

from src.adapters.driven.infra import db


class PeeweeWorker:
    def __enter__(self):
        # logger.debug("Opening database connection")
        # db.connect()
        logger.info("Beginning transaction")
        db.begin()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            logger.info("Committing transaction")
            db.commit()
        else:
            logger.info("Rolling back transaction")
            db.rollback()
        # logger.debug("Closing database connection")
        # db.close()
