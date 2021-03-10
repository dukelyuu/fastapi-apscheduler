from typing import Callable

from fastapi import FastAPI
from loguru import logger

# from src.db.events import close_db_connection, connect_to_db


def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app() -> None:
        # await connect_to_db(app)
        pass

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    @logger.catch
    async def stop_app() -> None:
        # await close_db_connection(app)
        pass
            
    return stop_app
