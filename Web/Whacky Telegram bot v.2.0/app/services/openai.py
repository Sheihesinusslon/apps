from dataclasses import dataclass
from typing import NewType

import openai
from openai import OpenAIError

from app.config import cfg, SERVICE_ERROR_MSG
from app.logger import logger

openai.api_key = cfg.OPENAI_TOKEN

ModelName = NewType("ModelName", str)


@dataclass
class GPT:
    """Instantiates a connection with OpenAI and provides an interface to communicate with it"""

    model_engine: ModelName = ModelName("text-davinci-003")
    max_tokens: int = 2048
    temperature: float = 0.5

    def generate_response(self, prompt: str) -> str:
        """Low-level function to generate a request, send it to the model and return the response back

        Args:
            prompt: user prompt

        Returns
            a string, a generated response from the service
        """
        logger.info("Sending a request to OpenAI.")
        try:
            completion = openai.Completion.create(
                engine=self.model_engine,
                prompt=prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
        except OpenAIError as err:
            logger.error(err)
            response = SERVICE_ERROR_MSG
        else:
            response = completion.choices[0].text

        return response

    def generate_random_response(self, prompt: str) -> str:
        """Top-level function to request a model to generate a random response for a requested user input

        Args:
            prompt: user prompt

        Returns:
            a string, a generated response from the service
        """
        prompt = "Generate random whacky response to the question: " + prompt
        return self.generate_response(prompt)

    def get_horoscope(self) -> str:
        """Top-level function that requests a model to generate a horoscope.
        Returns a generated response from a model
        """
        prompt = "Generate a random horoscope for the day in five sentences."
        return self.generate_response(prompt)
