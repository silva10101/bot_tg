from bot_create import dp, bot
from keyboards import kb_finance
from data_bases import bd_finance

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from datetime import datetime






class FSMFinance(StatesGroup):
    add = State()
    add_nday = State()
    delete = State()
    date = State()



async def finance_event(message : types.Message):
    await bot.send_message(message.from_user.id, 'Финансы!!!', reply_markup=kb_finance)


async def add_event(message : types.Message):
    """начало ввода добавления"""
    await bot.send_message(message.from_user.id, 'Введите данные:\n(Сумма(+/-), категорию(еда, ), описание)')
    await FSMFinance.add.set()

async def write_bd(message : types.Message, state: FSMContext):
    """Добавляем сумму"""
    data = message.text.split(' ')
    data.extend(datetime.now().strftime("%d %m %Y").split(' '))
    await bd_finance.sql_add_command(data) 
    await state.finish()
    await message.reply('Данные записаны')


async def add_nday_event(message : types.Message):
    """начало ввода добавления"""
    await bot.send_message(message.from_user.id, 'Введите данные:\n(Сумма(+/-), категорию(еда, ), описание, день, месяц, год)')
    await FSMFinance.add_nday.set()

async def write_nday_bd(message : types.Message, state: FSMContext):
    """Добавляем сумму"""
    data = message.text.split(' ')
    await bd_finance.sql_add_command(data) 
    await state.finish()
    await message.reply('Данные записаны')


async def delete_event(message : types.Message):
    """начало ввода удаления"""
    await bot.send_message(message.from_user.id, 'Введите данные\n(сумма, категория, день, месяц:')
    await FSMFinance.delete.set()

async def delete_bd(message : types.Message, state: FSMContext):
    """удаляем сумму"""
    data = message.text.split(' ')
    await bd_finance.sql_delete_command(data) 
    await state.finish()
    await message.reply('Данные удалены')


async def show_day(message : types.Message):
    """выводим статистику"""
    await bot.send_message(message.from_user.id, 'Введите день(дд мм гггг)')
    await FSMFinance.date.set()

async def show_day_finance(message : types.Message, state: FSMContext):
    """выводим данные дня"""
    data = message.text.split(' ')
    await bd_finance.sql_read_command(message, data)
    await state.finish()

async def show_today(message : types.Message):
    """выводим статистику сегодня"""
    data = datetime.now().strftime("%d %m %Y").split(' ')
    await bd_finance.sql_read_command(message, data)


async def cancel(message:types.Message,state:FSMContext):
    '''отмена'''
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Отменено')





def register_handlers(dp : Dispatcher):
    # Объявляем условия хендлеров
    dp.register_message_handler(finance_event, commands=['finance'])

    dp.register_message_handler(cancel, state='*', commands='отмена')
    dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True), state='*')

    dp.register_message_handler(add_event, commands=['add'], state=None)
    dp.register_message_handler(write_bd, state=FSMFinance.add)

    dp.register_message_handler(add_nday_event, commands=['add_nday'], state=None)
    dp.register_message_handler(write_nday_bd, state=FSMFinance.add_nday)

    dp.register_message_handler(delete_event, commands=['delete'], state=None)
    dp.register_message_handler(delete_bd, state=FSMFinance.delete)  

    dp.register_message_handler(show_day, commands=['nday_report'])
    dp.register_message_handler(show_day_finance, state=FSMFinance.date)
    dp.register_message_handler(show_today, commands=['today_report'])
















# class FSMFinance(StatesGroup):
#     amount = State()
#     description = State()
#     input_date = State()
#     input_date_for_delete = State()
#     input_data_for_delete = State()
#     deleting = State()


# async def finance_event(message : types.Message):
#     await bot.send_message(message.from_user.id, 'Финансы!!!', reply_markup=kb_finance)

# #====add=====

# async def add_income_event(message : types.Message):
#     """начало ввода дохода"""
#     global type_of_payment
#     type_of_payment = True
#     await bot.send_message(message.from_user.id, 'Введите сумму')
#     await FSMFinance.amount.set()

# async def add_expenses_event(message : types.Message):
#     """начало ввода расхода"""
#     global type_of_payment
#     type_of_payment = False
#     await bot.send_message(message.from_user.id, 'Введите сумму')
#     await FSMFinance.amount.set()

# async def remember_amount(message : types.Message, state: FSMContext):
#     """Добавляем сумму"""
#     async with state.proxy() as data:
#         data['amount'] = float(message.text)
#     await FSMFinance.next()
#     await message.reply('Введите описание')

# async def remember_description(message : types.Message, state: FSMContext):
#     """Описываем сумму"""
#     async with state.proxy() as data:
#         data['description'] = message.text
#         data['date'] = datetime.now().strftime("%d.%m.%Y")


#     if type_of_payment:
#         await bd_finance.sql_add_income_command(state)
#         await message.reply('доход добавлен', reply_markup=kb_finance)
#     else:
#         await bd_finance.sql_add_expenses_command(state)
#         await message.reply('расход добавлен', reply_markup=kb_finance)
#     await state.finish()

# #====delete=====

# async def delete_event(message : types.Message):
#     """начало удаления чего либо"""
#     await bot.send_message(message.from_user.id, 'Введите день(дд.мм.гггг)')
#     await bd_finance.sql_read_command(message, message.text)
#     global day
#     day = message.text
#     await FSMFinance.input_date_for_delete.set()

# async def input_day_for_delete(message : types.Message, state: FSMContext):
#     """выводим данные дня для удаления"""
#     await bot.send_message(message.from_user.id, 'Введите сумму-описание')
#     await FSMFinance.deleting.set()

# async def deleting_data(message : types.Message, state: FSMContext):
#     """удаление"""
#     await bd_finance.sql_delete_command(day, message)
#     await state.finish()

# #======output=====

# async def show_day(message : types.Message):
#     """выводим статистику дня"""
#     await bot.send_message(message.from_user.id, 'Введите день(дд.мм.гггг)')
#     await FSMFinance.input_date.set()

# async def show_day_finance(message : types.Message, state: FSMContext):
#     """выводим данные дня"""
#     await bd_finance.sql_read_command(message, message.text)
#     await state.finish()

# async def show_today(message : types.Message):
#     """выводим статистику сегодня"""
#     await bd_finance.sql_read_command(message, str(datetime.now().strftime("%d.%m.%Y")))


# #===============

# async def cancel(message:types.Message,state:FSMContext):
#     '''отмена'''
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.finish()
#     await message.reply('ok')




# # Объявляем условия хендлеров
# def register_handlers(dp : Dispatcher):
#     dp.register_message_handler(finance_event, commands=['finance'])
#     dp.register_message_handler(cancel, state='*', commands='отмена')
#     dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True), state='*')
#     dp.register_message_handler(add_income_event, commands=['add_income'], state=None)
#     dp.register_message_handler(add_expenses_event, commands=['add_expenses'], state=None)
#     dp.register_message_handler(delete_event, commands=['delete'])


#     dp.register_message_handler(show_today, commands=['today_report'])
#     dp.register_message_handler(show_day, commands=['nday_report'])


#     dp.register_message_handler(remember_amount, state=FSMFinance.amount)
#     dp.register_message_handler(remember_description, state=FSMFinance.description)
#     dp.register_message_handler(show_day_finance, state=FSMFinance.input_date)



#     dp.register_message_handler(delete_event, state=FSMFinance.input_date_for_delete)
#     dp.register_message_handler(input_day_for_delete, state=FSMFinance.input_data_for_delete)
#     dp.register_message_handler(deleting_data, state=FSMFinance.deleting)