import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)


class Client:
	signed = []
	waiting = []

	def __init__(self, id):
		self.id = id

	@staticmethod
	def show_keyboard(n: int):
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Записаться на Разговорный Клуб")
		item2 = types.KeyboardButton("Отказаться от участия")
		item3 = types.KeyboardButton("Да")
		item4 = types.KeyboardButton("Нет")
		item5 = types.KeyboardButton("/start")
		if n == 1:
			markup.add(item1)
			return markup
		elif n == 2:
			markup.add(item3, item4)
			return markup
		elif n == 3:
			markup.add(item2)
			return markup
		else:
			markup.add(item5)
			return markup


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
	file_id = 'CAACAgUAAxkBAAEBjDZfpW1LILCOSNQx69Q8e29SyuntEAACHAcAAszG4gLu8__0XRJBEx4E'
	bot.send_sticker(message.chat.id, file_id)

	bot.send_message(message.chat.id, "What\'s Up, <b>{0.first_name}</b>!\nЗдесь ты можешь записаться на Wake Up Event".format(message.from_user), parse_mode='html', reply_markup=Client.show_keyboard(1))


@bot.message_handler(content_types=['text'])
def reply(message):
	Client.id = message.chat.id
	Client.show_keyboard(1)

	if message.text == "Записаться на Разговорный Клуб":
		if not Client.id in Client.signed:
			Client.signed.append(Client.id)
			print(message.from_user.username)
			bot.send_message(Client.id, "Отлично, ждём", reply_markup=Client.show_keyboard(3))

		else:
			bot.send_message(Client.id, "Ты уже записан!", reply_markup=Client.show_keyboard(3))

	elif message.text == "Отказаться от участия":
		if Client.id in Client.signed:
			Client.signed.remove(Client.id)
			bot.send_message(Client.id, "Хорошо, ждём тебя в следующий раз", reply_markup=Client.show_keyboard(4))

		else:
			bot.send_message(Client.id, "Хорошо, ждём тебя в следующий раз", reply_markup=Client.show_keyboard(4))




# RUN
bot.polling(none_stop=True)
