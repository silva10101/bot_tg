from aiogram.types import ReplyKeyboardMarkup, KeyboardButton # ReplyKeyboardMarkup



button_add = KeyboardButton('/add')
button_add_nday = KeyboardButton('/add_nday')

button_nday_report = KeyboardButton('/nday_report')
button_today_report = KeyboardButton('/today_report')
button_delete = KeyboardButton('/delete')

button_cancel = KeyboardButton('/отмена')

button_balance = KeyboardButton('/balance')
button_month = KeyboardButton('/month_report')


kb_finance = ReplyKeyboardMarkup(resize_keyboard=True)

kb_finance.row(button_add, button_add_nday)
kb_finance.row(button_today_report, button_nday_report)
kb_finance.row(button_delete, button_cancel)
kb_finance.row(button_balance, button_month)




#from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ibutton_delete_income = InlineKeyboardButton('Удалить доход!', callback_data='delete_income')
# ibutton_delete_expences = InlineKeyboardButton('Удалить расход!', callback_data='delete_expences')

# ikb_income = InlineKeyboardMarkup()
# ikb_income.add(ibutton_delete_income)

# ikb_expences = InlineKeyboardMarkup()
# ikb_expences.add(ibutton_delete_expences)

