import telebot
from telebot import types
import config
from parse import word_of_the_day
from horoscop import horoscope, horoscop_keyboard
from UrbanDict import get_urban_definition, get_urban_words
from random import choice


def greeting():
	'''Generator of bot's greetings'''
	options = [
		"Aight, mate!\nWhat can I do for you??",
		"Ahoy, matey!\nWant a cup of coffee or a secret mission?",
		"This call may be recorded for training purposes.\nProceed, please.",
		"How does a lion greet the other animals in the field?\n- Pleased to eat you.",
		"Ghostbusters, whatya want?",
		"What's cookin', good lookin'?",
		"Hey there, freshman!\nWhat's good?",
		"Welcome to the club, boss!\nWhat's the plan?"
		"I came here to speak English and\nmeet my friend.\nAs you can see, I have spoken.",
		"Shhh, speak quiet,\nthey are watching us.\nWere you followed?",
		"Salutations are greetings!\nNeed something?",
		"Alright alright alright!",
		"Bot. James Bot.\nAnd you?",
		"You know what they say in China?\n They say: Ciao!"
	]
	return choice(options)

def main():
	bot = telebot.TeleBot(config.TOKEN)

	def start_keyboard():
		''' The main inline keyboard that the bot is going to reply every time '''
		# init keyboard and prepare keys
		keyboard = types.InlineKeyboardMarkup()
		key1 = types.InlineKeyboardButton(text="Say Hello", callback_data='Hello')
		key2 = types.InlineKeyboardButton(text="Get a Word of the Day", callback_data='Word')
		key3 = types.InlineKeyboardButton(text="Get a Horoscope for the day", callback_data='Horoscope')
		key4 = types.InlineKeyboardButton(text="Urban Dictionary", callback_data='Urban')
		# add keys to the keyboard
		keyboard.add(key1)
		keyboard.add(key2)
		keyboard.add(key3)
		keyboard.add(key4)

		return keyboard

	@bot.message_handler(commands=['start', 'help'])
	def welcome(message):
		file_id = 'CAACAgUAAxkBAAEBjDZfpW1LILCOSNQx69Q8e29SyuntEAACHAcAAszG4gLu8__0XRJBEx4E'
		bot.send_sticker(message.chat.id, file_id)
		msg = greeting()
		bot.send_message(message.chat.id, msg, reply_markup=start_keyboard())

	@bot.message_handler(content_types=['text'])
	def get_text_messages(message):
		''' Handle text messages from a user'''
		if message.text.startswith('Urban') or message.text.startswith('urban'):
			# if message starts with 'Urban', user sends commands to work with Urban Dictionary
			urban_command = message.text.split()
			if len(urban_command) == 1:
				# get 10 random Urban slangs
				msg = get_urban_words()
			else:
				# get Urban definition for a required word/phrase
				msg = get_urban_definition(' '.join(urban_command[1:]))
			bot.send_message(message.chat.id, msg, reply_markup=start_keyboard(), parse_mode='html')
		else:
			# Send a welcome message with the initial inline keyboard in response to any other text message from a user
			welcome(message)

	@bot.callback_query_handler(func=lambda call: True) 
	def callback_worker(call):
		''' Inline keyboard message handler '''
		if call.data == 'Urban':
			bot.send_message(call.message.chat.id, 'Send <b>Urban</b> to get 10 random\nwords/phrases from Urban Dictionary\n\n'
														'Send <b>Urban "your word/phrase"</b>\nto get Urban definition\n', 
													parse_mode='html', reply_markup=start_keyboard())

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
