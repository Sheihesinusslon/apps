from aiogram import Bot, Dispatcher, executor, types
from vk_parse import VkParser
from client import ClientDispatcher
from subscript import Subscription
import asyncio
import aioschedule
import logging
import time
import config

# set level of logs
logging.basicConfig(level=logging.INFO)

# init bot and create loop
loop = asyncio.get_event_loop()
bot = Bot(config.TOKEN, loop)
dp = Dispatcher(bot)
# init ClientDispatcher
Client = ClientDispatcher()
# init parser
vk = VkParser()
# init bd connection
db = Subscription('subscriptions.db')


@dp.message_handler(commands=['начало', 'help'])
async def welcome(message: types.Message):
	''' Welcome-start message with all options for a user:
	subscribe, unsubscribe, sign in, sign out for the event '''
	id = message.from_user.id
	file_id = 'CAACAgUAAxkBAAEBjDZfpW1LILCOSNQx69Q8e29SyuntEAACHAcAAszG4gLu8__0XRJBEx4E'
	await message.answer_sticker(file_id)
	await message.answer("What\'s Up, <b>{0.first_name}</b>!\n"
						 "Здесь ты можешь записаться на Разговорный клуб.\n\n"
						 "Также ты можешь подписаться на рассылку о событии, чтобы получать новости о проведении клуба :)"
						 "\n\n"
						 "/subscribe - Подписаться на рассылку\n"
						 "/unsubscribe - Отписаться от рассылки"
                         .format(message.from_user),
						 parse_mode='html',
						 reply_markup=Client.show_keyboard(1))


@dp.message_handler(content_types=['text'])
async def reply(message: types.Message):
	id = message.from_user.id
	if message.text == "Записаться на Разговорный Клуб":
		if Client.available_to_signup():
			if id not in Client.signed:
				# if client is signing up first time, automatically send info about the event from VK group
				await message.answer(text=send_post_text(),
									 parse_mode='html')
			await signup(message, id)
		else:
			if id not in Client.signed:
				# if max capacity for the event reached, suggest to stay in waiting list in case
				# somebody will sign out
				await message.answer('Записалось максимальное количество участников. '
									 'Мы можем добавить тебя в лист ожидания и сообщить, если освободится местечко.\n\n'
									 'Добавить тебя в лист ожидания?',
									 reply_markup=Client.show_keyboard(3))
			else:
				# if user is signed up and trying to do it again
				await message.answer("Ты уже записан(a)!",
									 reply_markup=Client.show_keyboard(2))

	elif message.text == "Отказаться от участия":
		await signout(message, id)

	elif message.text == "/subscribe":
		await subscribe(message)

	elif message.text == "/unsubscribe":
		await unsubscribe(message)

	# "Yeah!/Nope" handle two cases: when suggesting a user to stay in the waiting list and
	# when suggesting a subscribed user to sign up when a new post about the event is published
	elif message.text == "Yeah!":
		if Client.available_to_signup():
			await signup(message, id)
		else:
			await put_in_waiting_list(message, id)

	elif message.text == "Nope":
		await message.answer("Хорошо, ждём тебя в следующий раз",
							 reply_markup=Client.show_keyboard(1))

	# Two manager's commands to confirm/dismiss operation of event cancellation
	elif message.text == 'да' and id == Client.manager_id:
		await _cancel_event()
		await message.answer('Начинаю рассылку об отмене ...')

	elif message.text == 'нет' and id == Client.manager_id:
		await message.answer('Отмена не состоялась')


def send_post_text():
	'''Function to send message with data from vk's post'''
	if not vk.data:
		vk.last_post()
	info = vk.data
	text = info['text']
	media = '<a href="{0}">Media</a>'.format(info['url_att'])
	link = '<a href="{0}">Источник ВК</a>'.format(info['link'])
	try:
		return f'{text}\n{media}\n{link}'
	except Exception as e:
		# if there are errors with parsing an attachment from the VK group, just send data without it
		print(e)
		return f'{text}\n{link}'


async def signup(message, id):
	if id not in Client.signed:
		Client.signed.append(id)
		await message.answer("Будем ждать тебя!",
							 reply_markup=Client.show_keyboard(2))
		print(f'{message.from_user.username} записался.\n'
			  f'Всего записавшихся: {len(Client.signed)}\n')
	else:
		await message.answer("Ты уже записан(a)!",
							 reply_markup=Client.show_keyboard(2))


async def put_in_waiting_list(message, id):
	if id not in Client.waiting:
		Client.waiting.append(id)
		await message.answer('Ok! Мы напишем тебе, если кто-то откажется :)',
							 reply_markup=Client.show_keyboard(2))
		print(f'{message.from_user.username} добавлен в лист ожидания.\n'
			  f'Всего ожидает: {len(Client.waiting)}\n')
	else:
		await message.answer('Ты и так уже в листе ожидания!',
							 reply_markup=Client.show_keyboard(2))


async def signout(message, id):
	if id in Client.signed:
		Client.signed.remove(id)
	if id in Client.waiting:
		Client.waiting.remove(id)
	await message.answer("Хорошо, ждём тебя в следующий раз",
						 reply_markup=Client.show_keyboard(1))
	print(f'{message.from_user.username} отказался от участия.\n'
		  f'Всего записавшихся: {len(Client.signed)}\n'
		  f'В листе ожидания: {len(Client.waiting)}\n')


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
	''' Function to subscribe for event updates '''
	if not db.subscriber_exists(message.from_user.id):
		# if user is not in db, add them
		db.add_subscriber(message.from_user.id)
	else:
		# if user is in db, update subscription status
		db.update_subscription(message.from_user.id, True)
	await message.answer("Ты успешно подписан(а) на рассылку!",
						 reply_markup=Client.show_keyboard(1))


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
	''' Function to unsubscribe from event updates '''
	if (not db.subscriber_exists(message.from_user.id)):
		# if user is not in db, add them with inactive subscription status (remember)
		db.add_subscriber(message.from_user.id, False)
		await message.answer("Ты итак не подписан(а).",
							 reply_markup=Client.show_keyboard(1))
	else:
		# if user is in db, update subscription status
		db.update_subscription(message.from_user.id, False)
		await message.answer("Ты успешно отписан(а) от рассылки.",
							 reply_markup=Client.show_keyboard(1))


async def scheduler(interval):
	''' Function manages several routines: clears signed and waiting lists after the event,
	 notifies subscribed users about event updates, checks for signed out users, sends info to
	 an event manager, suggests the manager to cancel the event if very few people signed up'''
	aioschedule.every().day.at('18:00').do(notify)
	aioschedule.every().monday.do(Client.clear_lists)
	aioschedule.every().minute.do(check_vacant_spot)
	aioschedule.every(6).hours.do(send_info_to_manager)
	aioschedule.every().saturday.at('10:00').do(cancel_event)
	while True:
		await aioschedule.run_pending()
		await asyncio.sleep(interval)


async def notify():
	''' Function checks for updates from VK group and, if there is, sends info to subscribed
	users and suggests to sign up for the event '''
	new_post = vk.last_post()
	if new_post:
		subscriptions = db.get_subscriptions()
		for subscribed in subscriptions:
			await bot.send_message(subscribed[1],
								   text=send_post_text(),
								   parse_mode='html')
			await bot.send_message(subscribed[1],
								   'Записать тебя?',
								   reply_markup=Client.show_keyboard(3))


async def check_vacant_spot():
	''' Function sends a message to users in waiting list, if somebody signed out '''
	if Client.available_to_signup() and len(Client.waiting) > 0:
		id = Client.waiting[0]
		await bot.send_message(id,
							   'Освободилось место на Разговорный клуб.\n'
							   'Записать тебя?', reply_markup=Client.show_keyboard(3))


async def send_info_to_manager():
	''' Function sends report to the event manager with info about signed and waiting users '''
	id = Client.manager_id
	await bot.send_message(id,
						   text=Client.report())


async def cancel_event():
	''' Function sends a message to the event manager with a suggestion to cancel the event
	if minimal capacity for the event hasn't reached '''
	id = Client.manager_id
	if len(Client.signed) < 5:
		await bot.send_message(id,
							   text='Записалось слишком мало желающих.\n'
											   'Отменить эвент? да/нет')

async def _cancel_event():
	''' Function sends a message about an event cancellation after confirm message from the event manager'''
	for id in Client.signed:
		await bot.send_message(id,
							   'Хэй! На клуб записалось слишком мало желающих.\n'
							   'Мы отменяем встречу на этой неделе. Hope to see you next time!',
							   reply_markup=Client.show_keyboard(1))


# run long polling
if __name__ == '__main__':
	loop.create_task(scheduler(1))
	executor.start_polling(dp, skip_updates=True)

