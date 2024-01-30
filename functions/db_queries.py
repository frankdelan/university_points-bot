from datetime import datetime

from .db_connector import make_crud_query, make_query


@make_crud_query
async def add_student(user_id: str, email: str, password: str) -> str | None:
    return "INSERT INTO students (id, email, password) " \
           f"VALUES ('{user_id}', '{email}', '{password}')"


@make_query
async def get_students_id():
    return "SELECT id " \
            "FROM students"


@make_query
async def find_user(user_id: str) -> str | list[tuple[datetime]]:
    return "SELECT COUNT(*) as count " \
            "FROM students " \
            f"WHERE id='{user_id}'"


async def check_user(user_id: str) -> bool:
    result = await find_user(user_id)
    if result[0][0]:
        return True
    else:
        return False


@make_query
async def get_student_data(user_id: str) -> str | list[tuple[datetime]]:
    return "SELECT id, email, password " \
            "FROM students " \
            f"WHERE id='{user_id}'"


@make_query
async def get_date(user_id: str) -> str | list[tuple[datetime]]:
    return "SELECT date " \
            "FROM students " \
            f"WHERE id='{user_id}'"


@make_crud_query
async def update_date(user_id: str, date: datetime) -> str | None:
    return "UPDATE students " \
            f"SET date = '{date}'" \
            f"WHERE id='{user_id}'"


@make_crud_query
async def change_user_data(user_id: str, email: str, password: str) -> str | None:
    return "UPDATE students " \
            f"SET email = '{email}', password = '{password}'" \
            f"WHERE id='{user_id}'"




print("В")