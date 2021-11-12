import random
from telebot import types


def horoscope() -> str:
    ''' Send a text with a horoscope '''
    first = ["\nСегодня — идеальный день для новых начинаний.","\nОптимальный день для того, чтобы решиться на смелый поступок!","\nБудьте осторожны, сегодня звёзды могут повлиять на ваше финансовое состояние.","\nЛучшее время для того, чтобы начать новые отношения или разобраться со старыми.","\nПлодотворный день для того, чтобы разобраться с накопившимися делами."]
    second = ["Но помните, что даже в этом случае нужно не забывать про","Если поедете за город, заранее подумайте про","Те, кто сегодня нацелен выполнить множество дел, должны помнить про","Если у вас упадок сил, обратите внимание на","Помните, что мысли материальны, а значит вам в течение дня нужно постоянно думать про"]
    second_add = ["отношения с друзьями и близкими.","работу и деловые вопросы, которые могут так некстати помешать планам.","себя и своё здоровье, иначе к вечеру возможен полный раздрай.","бытовые вопросы — особенно те, которые вы не доделали вчера.","отдых, чтобы не превратить себя в загнанную лошадь в конце месяца."]
    third = ["Злые языки могут говорить вам обратное, но сегодня их слушать не нужно.","Знайте, что успех благоволит только настойчивым, поэтому посвятите этот день воспитанию духа.","Даже если вы не сможете уменьшить влияние ретроградного Меркурия, то хотя бы доведите дела до конца.","Не нужно бояться одиноких встреч — сегодня то самое время, когда они значат многое.","Если встретите незнакомца на пути — проявите участие, и тогда эта встреча посулит вам приятные хлопоты."]

    return random.choice(first) + ' ' + random.choice(second) + ' ' + random.choice(second_add) + ' ' + random.choice(third)


def horoscop_keyboard():
    ''' Prepare keys for inline keyboard, return keyboard '''
    # init keyboard
    keyboard = types.InlineKeyboardMarkup()
    # prepare keys
    key_oven = types.InlineKeyboardButton(text='Овен', callback_data='zodiac')
    key_telec = types.InlineKeyboardButton(text='Телец', callback_data='zodiac')
    key_bliznecy = types.InlineKeyboardButton(text='Близнецы', callback_data='zodiac')
    key_rak = types.InlineKeyboardButton(text='Рак', callback_data='zodiac')
    key_lev = types.InlineKeyboardButton(text='Лев', callback_data='zodiac')
    key_deva = types.InlineKeyboardButton(text='Дева', callback_data='zodiac')
    key_vesy = types.InlineKeyboardButton(text='Весы', callback_data='zodiac')
    key_scorpion = types.InlineKeyboardButton(text='Скорпион', callback_data='zodiac')
    key_strelec = types.InlineKeyboardButton(text='Стрелец', callback_data='zodiac')
    key_kozerog = types.InlineKeyboardButton(text='Козерог', callback_data='zodiac')
    key_vodoley = types.InlineKeyboardButton(text='Водолей', callback_data='zodiac')
    key_ryby = types.InlineKeyboardButton(text='Рыбы', callback_data='zodiac')
    # add keys to keyboard
    keyboard.add(key_oven, key_telec)
    keyboard.add(key_bliznecy, key_rak)
    keyboard.add(key_lev, key_deva)
    keyboard.add(key_vesy, key_scorpion)
    keyboard.add(key_strelec, key_kozerog)
    keyboard.add(key_vodoley, key_ryby)


    return keyboard
