import asyncpg
from functools import wraps
from config import db


async def get_connection():
    return await asyncpg.connect(
        database=db["database"],
        host=db["host"],
        user=db["user"],
        password=db["password"],
        port=db["port"])


def make_crud_query(func):
    @wraps(func)
    async def wrapper(*args):
        connection = await get_connection()
        try:
            sql = await func(*args)
            async with connection.transaction():
                await connection.execute(sql)
        finally:
            await connection.close()
    return wrapper


def make_query(func):
    @wraps(func)
    async def wrapper(*args):
        connection = await get_connection()
        try:
            sql = await func(*args)
            result = await connection.fetch(sql)
            return result
        finally:
            await connection.close()
    return wrapper
