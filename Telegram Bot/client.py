from aiogram import types


class ClientDispatcher:
	''' Helper class to manage users and provide keyboard configurations '''
	manager_id = 343604792   # event manager user id in Telegram

	def __init__(self):
		self.signed = []
		self.waiting = []
		self.capacity = 13

	def report(self):
		''' Info about signed clients that is being sent to event manager by the bot '''
		report = ['REPORT'.center(16, '*')]
		report.append(f'Записалось:{0: 5}'.format(len(self.signed)))
		if self.waiting:
			report.append(f'Ожидает:{0: 8}'.format(len(self.waiting)))
		return '\n'.join(report)

	def available_to_signup(self):
		return len(self.signed) < self.capacity

	async def clear_lists(self):
		self.signed.clear()
		self.waiting.clear()
		print('Lists are cleared.')

	@staticmethod
	def show_keyboard(n: int):
		''' Keyboard configurations shown to the user '''
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Записаться на Разговорный Клуб")
		item2 = types.KeyboardButton("Отказаться от участия")
		item3 = types.KeyboardButton("/начало")
		item4 = types.KeyboardButton("Yeah!")
		item5 = types.KeyboardButton("Nope")
		if n == 1:
			markup.add(item1).add(item2).add(item3)
		elif n == 2:
			markup.add(item2, item3)
		elif n == 3:
			markup.add(item4, item5).add(item3)
		else:
			markup.add(item3)
		return markup

