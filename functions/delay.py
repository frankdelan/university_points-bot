from datetime import datetime
from functions import get_date, update_date


async def compare_time(user_id: str) -> bool:
    cur_datetime: datetime = datetime.now()
    last_date: list | datetime = await get_date(user_id)
    last_date = last_date[0][0]
    if cur_datetime.year > last_date.year or cur_datetime.month > last_date.month:
        await update_date(user_id, cur_datetime)
        return True
    elif cur_datetime.day > last_date.day or cur_datetime.hour > last_date.hour:
        await update_date(user_id, cur_datetime)
        return True
    elif cur_datetime.minute - last_date.minute >= 5:
        await update_date(user_id, cur_datetime)
        return True
    else:
        return False
