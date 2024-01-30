from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from keyboards import choose_decade_keyboard, menu_keyboard
from functions import check_user, collect_data, compare_time


class Decade(StatesGroup):
    get_a_decade = State()


async def get_a_decade(message: types.Message):
    if message.text == 'Баллы' and await check_user(str(message.from_user.id)):
        await message.answer("Выберите семестр: ", reply_markup=choose_decade_keyboard)
        await Decade.get_a_decade.set()
    else:
        await message.answer('Вы не зарегистрированы!',
                             reply_markup=menu_keyboard)


async def get_a_points(message: types.Message, state: FSMContext):
    await state.update_data(decade=int(message.text))
    my_data = await state.get_data()
    student_id: str = str(message.from_user.id)
    is_delay: bool = await compare_time(student_id)
    if 1 <= int(my_data['decade']) <= 8:
        if not is_delay:
            await message.answer('Баллы можно смотреть раз в 5 минут!\nНемного подождите.',
                                 reply_markup=menu_keyboard)
        else:
            await message.answer(f'Данные загружаются, немного подождите..',
                                 reply_markup=menu_keyboard)
            all_data = await collect_data(my_data['decade'], student_id)
            await message.answer(f'{all_data}')
        await state.finish()
    else:
        await message.answer(f'Данный семестр не найден.',
                             reply_markup=menu_keyboard)
        await state.finish()


def setup_points(dp: Dispatcher):
    dp.register_message_handler(get_a_decade, text='Баллы')
    dp.register_message_handler(get_a_points, state=Decade.get_a_decade)
