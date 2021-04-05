import telebot
from telebot import types
import config
from parse import word_of_the_day
from horoscop import horoscope, horoscop_keyboard


def main():
	bot = telebot.TeleBot(config.TOKEN)

	def start_keyboard():
		''' The main inline keyboard that the bot is going to reply every time '''
		# init keyboard and prepare keys
		keyboard = types.InlineKeyboardMarkup()
		key1 = types.InlineKeyboardButton(text="Say Hello", callback_data='Hello')
		key2 = types.InlineKeyboardButton(text="Get a Word of the Day", callback_data='Word')
		key3 = types.InlineKeyboardButton(text="Get a Horoscope for the day", callback_data='Horoscope')
		# add keys to the keyboard
		keyboard.add(key1)
		keyboard.add(key2)
		keyboard.add(key3)

		return keyboard

	@bot.message_handler(commands=['start', 'help'])
	def welcome(message):
		file_id = 'CAACAgUAAxkBAAEBjDZfpW1LILCOSNQx69Q8e29SyuntEAACHAcAAszG4gLu8__0XRJBEx4E'
		bot.send_sticker(message.chat.id, file_id)
		bot.send_message(message.chat.id, "Aight, mate!\nWhat can I do for you??", reply_markup=start_keyboard())

	@bot.message_handler(content_types=['text'])
	def get_text_messages(message):
		''' Send a welcome message with the initial inline keyboard in response to any text message from a user'''
		if message.text:
			welcome(message)

	@bot.callback_query_handler(func=lambda call: True) 
	def callback_worker(call):
		''' Inline keyboard message handler '''
		if call.data == 'Horoscope':
			bot.send_message(call.message.chat.id, 'Choose your patronus >>>', reply_markup=horoscop_keyboard())

		if call.data == "zodiac":
			msg = horoscope()
			bot.send_message(call.message.chat.id, msg, reply_markup=start_keyboard())

		if call.data == 'Hello':
			bot.send_sticker(call.message.chat.id, 'CAACAgUAAxkBAAEB75NgPIf6qBFn7oIn1yabOuFiQyZMiAACGAcAAszG4gK5TgnCYv-AgR4E')
			with open('greeting.ogg', 'rb') as voice:
				bot.send_voice(call.message.chat.id, voice=voice, reply_markup=start_keyboard())

		if call.data == 'Word':
			try:
				msg = word_of_the_day()
			except:
				msg = 'Feel bad now. Try later ...'
			finally:
				bot.send_message(call.message.chat.id, msg, parse_mode='html', reply_markup=start_keyboard())

	bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
	print('Бот запущен ...')
	main()
