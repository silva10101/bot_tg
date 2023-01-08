from bot_create import dp
from data_bases import bd_finance
from aiogram.utils import executor




async def on_startup(_):
    print('Бот запущен')
    bd_finance.db_finance_start()

from handlers import handler_start, handler_finance


handler_start.register_handlers(dp)
handler_finance.register_handlers(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
