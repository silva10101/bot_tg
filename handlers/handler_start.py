from bot_create import dp, bot
from keyboards import kb_start

from aiogram import types, Dispatcher




async def start_event(message : types.Message):
    await bot.send_message(message.from_user.id, 'Привет, держи меню', reply_markup=kb_start)



# Объявляем условия хендлеров
def register_handlers(dp : Dispatcher):
    dp.register_message_handler(start_event, commands=['start'])