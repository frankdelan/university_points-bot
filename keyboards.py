from aiogram.types import ReplyKeyboardMarkup

register_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
register_keyboard.add('Регистрация')

choose_decade_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
choose_decade_keyboard.add('1', '2', '3')
choose_decade_keyboard.add('4', '5', '6')
choose_decade_keyboard.add('7', '8')

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add('Баллы', 'Изменить данные')
