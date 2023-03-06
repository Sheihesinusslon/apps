import telebot
from app.config import cfg
from app.logger import logger
from app.services.whacky_bot import WhackyBot, WhackyTeleBot
from app.utils import KeyboardManager, Bot


def run_bot(bot: Bot, whacky_bot: WhackyBot):
    """Runs bot and activates its interface"""
    @bot.message_handler(commands=[whacky_bot.START, whacky_bot.HELP])
    def welcome(message):
        return whacky_bot.welcome(message)

    @bot.message_handler(commands=[whacky_bot.GPT])
    def gpt_command(message):
        return whacky_bot.handle_gpt_request(message)

    @bot.message_handler(commands=[whacky_bot.URBAN])
    def urban_command(message):
        return whacky_bot.handle_ud_request(message)

    @bot.message_handler(content_types=['text'], regexp=f"^{whacky_bot.URBAN}.*")
    def handle_ud_request(message):
        return whacky_bot.handle_ud_request(message)

    @bot.message_handler(content_types=['text'], regexp=f"^{whacky_bot.GPT}.*")
    def handle_gpt_request(message):
        return whacky_bot.handle_gpt_request(message)

    @bot.message_handler(content_types=['text'])
    def handle_text_messages(message):
        return whacky_bot.handle_text_messages(message)

    @bot.callback_query_handler(func=lambda call: True)
    def handle_keyboard_messages(call):
        return whacky_bot.handle_keyboard_messages(call)

    whacky_bot.run_bot()


def main():
    """Creates a bot instance and runs it"""
    bot = telebot.TeleBot(cfg.BOT_TOKEN, colorful_logs=True, parse_mode="markdown")
    keyboard = KeyboardManager(keyboard=telebot.types.InlineKeyboardMarkup(), button=telebot.types.InlineKeyboardButton)
    whacky_bot: WhackyBot = WhackyTeleBot(bot=bot, keyboard_manager=keyboard)

    run_bot(bot, whacky_bot)


if __name__ == "__main__":
    logger.info("Bot started ...")
    main()
