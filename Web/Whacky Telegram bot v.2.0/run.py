from app import init_bot_factory
from app.config import BotConfig
from app.logger import logger
from app.interfaces import ITeleBot, IWhackyBot


def run_bot(bot: ITeleBot, whacky_bot: IWhackyBot):
    """Function-adapter that delegates interface calls for Telebot library to WhackyBot"""
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


if __name__ == "__main__":
    cfg = BotConfig.get_config()
    whacky_bot: IWhackyBot = init_bot_factory(cfg)
    run_bot(whacky_bot.bot, whacky_bot)
    logger.info("Bot started ...")
