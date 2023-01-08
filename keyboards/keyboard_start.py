from aiogram.types import ReplyKeyboardMarkup, KeyboardButton # ReplyKeyboardMarkup



button_finance = KeyboardButton('/finance')

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.add(button_finance)
