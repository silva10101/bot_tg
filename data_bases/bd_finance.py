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


async def sql_delete_command(data):
	cur.execute(f"""DELETE FROM money WHERE 
		amount = '{data[0]}' AND 
		category = '{data[1]}' AND
		day = '{data[2]}' AND
		month = '{data[3]}'""").fetchall()
	base.commit()
	print('удалил', data)

