from requests import RequestException
from telebot.apihelper import ApiTelegramException
from udpy import UrbanClient

from app.config import SERVICE_ERROR_MSG
from app.logger import logger


class UrbanDict:
    """Class responsible for connection instantiation with Urban Dictionary service using udpy library.
        Calls UrbanClient API to get responses from Urban Dictionary.
    """
    def __init__(self):
        logger.info("Initializing connection with UrbanClient.")
        self.client = UrbanClient()

    def get_definitions(self, prompt: str) -> str:
        """Top-level function responsible to dispatch the request between other class functions based on the
            user prompt.

        Args:
            prompt: user input

        Returns:
            a string, response message
        """
        # if message starts with 'Urban', user sends commands to work with Urban Dictionary
        if not prompt:
            # get 10 random Urban slangs
            msg = self.get_random_urban_words()
        else:
            # get Urban definition for a required word/phrase
            msg = self.get_urban_definition(prompt)

        return msg

    def get_urban_definition(self, word_or_phrase: str) -> str:
        """Function sends a request to UD to get a definition for a provided word or phrase
            and returns a text or unsuccessful notification

        Args:
              word_or_phrase: a word or phrase to look up to in the dictionary

        Returns:
            a string, response message: definitions or unsuccessful notification
        """
        try:
            logger.info("Sending request to UrbanClient.")
            defs = self.client.get_definition(word_or_phrase)
        except RequestException as err:
            logger.error(err)
            response = SERVICE_ERROR_MSG
        else:
            response = "".join(
                f"\n<b>{word_or_phrase}</b>\n" + d.definition.replace("[", "").replace("]", "") + "\n" for d in defs[:5]
            )

        return response or "Couldn't find a definition for your request :/"

    def get_random_urban_words(self) -> str:
        """Function sends a request for 10 random slangs to UD and returns a text

        Returns:
            a string, response message, 10 random urban slangs
        """
        try:
            logger.info("Sending request to UrbanClient.")
            rand = self.client.get_random_definition()
        except RequestException as err:
            logger.error(err)
            response = SERVICE_ERROR_MSG
        else:
            response = "\n".join(f"\n<b>{d.word}</b>\n" + d.definition.replace("[", "").replace("]", "") for d in rand)

        return response
