import asyncio
import logging
from bs4 import BeautifulSoup, Tag
import fake_useragent
import aiohttp

from config import login_url, main_link
from create_bot import bot
from functions import get_student_data, get_students_id

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('bot')


# async def check_website_changes() -> None:
#     prev_data: dict = {}
#     while True:
#         student_data: dict = {idx[0]: "" for idx in await get_students_id()}
#         for idx in student_data.keys():
#             points: str = await collect_data('7', idx)
#             student_data[idx] = points
#         if prev_data:
#             for idx1, idx2 in zip(student_data.keys(), prev_data.keys()):
#                 if student_data[idx1] == prev_data[idx2]:
#                     await asyncio.sleep(3600)
#                 else:
#                     await bot.send_message(idx1, student_data[idx1], parse_mode='html')
#         prev_data = student_data.copy()


def get_header_data() -> dict[str, str]:
    user = fake_useragent.UserAgent()
    header = {
        'user-agent': user.random
    }
    return header


async def connect(user_id: str) -> tuple[str, int] | None:
    header = get_header_data()
    student_data: list = await get_student_data(user_id)
    user_data = {'LoginForm[identity]': student_data[0][1],
                 'LoginForm[password]': student_data[0][2]}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(login_url, data=user_data, headers=header, ssl=False):
                # ssl=False использую пока на сайте не подтвержден сертификат
                async with session.get(main_link, ssl=False) as response:
                    data = await response.text(), response.status
                    return data
    except aiohttp.ClientSession as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        return None


async def collect_data(decade: str, user_id: str) -> str:
    data_points = await connect(user_id)
    if data_points[1] != 200:
        return "Сайт временно недоступен!"

    soup = BeautifulSoup(data_points[0], 'lxml')
    element = soup.find('div', id=f'tab-0-{int(decade) - 1}')

    if element is None:
        logger.error(f"Пользователь ввёл неверный логин или пароль.")
        return "Ошибка! Неверный логин или пароль!"
    else:
        subjects: list[Tag] = element.find('tbody').find_all(
            'tr')
        result: str = get_points_by_subject(subjects)
        return result


def get_points_by_subject(subjects: list[Tag]) -> str:
    result: str = ''
    for subject in subjects:
        subject_data = [subject.find_all('td')[index].text for index in range(11)]
        result += f'__________________\n' \
                  f'Предмет: {subject_data[1]} ({subject_data[2]})\n\n' \
                  f'Первый модуль: {subject_data[3]}\n' \
                  f'Второй модуль: {subject_data[4]}\n' \
                  f'Третий модуль: {subject_data[5]}\n' \
                  f'Итоги: {subject_data[6].split()[0]}\n' \
                  f'Экзамен: {subject_data[7]}\n' \
                  f'Пересдача: {subject_data[8]}\n' \
                  f'Комиссия: {subject_data[9]}\n' \
                  f'Оценка: {subject_data[10]}\n' \
                  f'__________________'
    logger.info(f"Данные получены.")
    return result
