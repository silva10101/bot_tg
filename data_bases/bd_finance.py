import sqlite3 as sq 


from bot_create import bot



def db_finance_start():
	global base, cur
	base = sq.connect('base_finance.db')
	cur = base.cursor()
	if base:
		print('База данных финансов подключена')
	base.execute('''CREATE TABLE IF NOT EXISTS money(
		amount TEXT,
		category TEXT, 
		description TEXT, 
		day TEXT, 
		month TEXT, 
		year TEXT)''')
	base.commit()


async def sql_add_command(data):
	cur.execute('INSERT INTO money VALUES (?, ?, ?, ?, ?, ?)', tuple(data))
	base.commit()
	print('добавил', data)


async def sql_read_command(message, data):
	await bot.send_message(message.from_user.id, 'Доходы')
	for ret in cur.execute(f"SELECT amount, category, description FROM money WHERE day='{data[0]}' AND month='{data[1]}' AND year='{data[2]}' AND amount > 0").fetchall():
		await bot.send_message(message.from_user.id, f'{ret[0]}руб. \tКатегория: {ret[1]}\nОписание: {ret[2]}\n')
	await bot.send_message(message.from_user.id, 'Расходы')
	for ret in cur.execute(f"SELECT amount, category, description FROM money WHERE day='{data[0]}' AND month='{data[1]}' AND year='{data[2]}' AND amount < 0").fetchall():
		await bot.send_message(message.from_user.id, f'{ret[0]}руб. \tКатегория: {ret[1]}\nОписание: {ret[2]}\n')


async def sql_read_m_command(message, data):
	category_income_set = set()
	category_expences_set = set()
	sum_i = 0
	sum_e = 0
	for ret in cur.execute(f"SELECT category FROM money WHERE month='{data[0]}' AND year='{data[1]}' AND amount > 0").fetchall():
		category_income_set.add(ret[0])
	for ret in cur.execute(f"SELECT category FROM money WHERE month='{data[0]}' AND year='{data[1]}' AND amount < 0").fetchall():
		category_expences_set.add(ret[0])

	message_for_user = 	'Доходы за месяц\n'
	for cat in category_income_set:
		for ret in cur.execute(f"SELECT amount FROM money WHERE category='{cat}'").fetchall():
			sum_i += float(ret[0])
		message_for_user += f'{cat}: {sum_i:.2f} руб.\n'

	message_for_user += 'Расходы за месяц\n'
	for cat in category_expences_set:
		for ret in cur.execute(f"SELECT amount FROM money WHERE category='{cat}'").fetchall():
			sum_e += float(ret[0])
		message_for_user += f'{cat}: {sum_e:.2f} руб.\n'
	message_for_user += f'Итого за месяц: {sum_e+sum_i:.2f}\n'
	await bot.send_message(message.from_user.id, message_for_user)

async def sql_delete_command(data):
	cur.execute(f"""DELETE FROM money WHERE 
		amount = '{data[0]}' AND 
		category = '{data[1]}' AND
		day = '{data[2]}' AND
		month = '{data[3]}'""").fetchall()
	base.commit()
	print('удалил', data)

