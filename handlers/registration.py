from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from keyboards import menu_keyboard, register_keyboard
from functions import check_user, add_student, change_user_data


class Register(StatesGroup):
    get_email = State()
    get_password = State()


class Change(StatesGroup):
    change_email = State()
    change_password = State()


async def bot_start(message: types.Message):
    if await check_user(str(message.from_user.id)):
        await message.answer("Вы используете бота для просмотра баллов!", reply_markup=menu_keyboard)
    else:
        await message.answer('Пройдите регистрацию', reply_markup=register_keyboard)


async def register_user(message: types.Message):
    if await check_user(str(message.from_user.id)):
        await message.answer("Вы уже зарегистрированы!", reply_markup=menu_keyboard)
    else:
        await message.answer("Введите почту")
        await Register.get_email.set()


async def get_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите пароль")
    await Register.get_password.set()


async def get_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    student_data: dict = await state.get_data()
    await add_student(message.from_user.id, student_data['email'], student_data['password'])
    await message.answer("Вы зарегистрированы!", reply_markup=menu_keyboard)
    await state.finish()


async def change_data(message: types.Message):
    if await check_user(str(message.from_user.id)):
        await message.answer("Введите новый email", reply_markup=menu_keyboard)
        await Change.change_email.set()
    else:
        await message.answer('Вы не зарегистрированы!', reply_markup=register_keyboard)


async def change_email(message: types.Message, state: FSMContext):
    await state.update_data(new_email=message.text)
    await message.answer('Введите новый пароль')
    await Change.change_password.set()


async def change_password(message: types.Message, state: FSMContext):
    await state.update_data(new_password=message.text)
    student_data: dict = await state.get_data()
    await change_user_data(message.from_user.id, student_data['new_email'], student_data['new_password'])
    await message.answer('Данные изменены!')
    await state.finish()


def setup_registration(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=['start'])
    dp.register_message_handler(register_user, text='Регистрация')
    dp.register_message_handler(get_email, state=Register.get_email)
    dp.register_message_handler(get_password, state=Register.get_password)
    dp.register_message_handler(change_data, text='Изменить данные')
    dp.register_message_handler(change_email, state=Change.change_email)
    dp.register_message_handler(change_password, state=Change.change_password)
