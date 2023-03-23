import logging
import os

import openai


class OpenAI:
    """
    OpenAI API wrapper
    """

    _openai: openai

    def __init__(self):
        self._openai = openai
        self._openai.api_key = os.environ["OPENAI_API_KEY"]

    def answer(self, prompt: str):
        response = self._openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=1000,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=["\n\n\n"],
        )
        response_text = response["choices"][0]["text"].strip()
        logging.info(f"[OpenAI] response: {response_text}")
        return response_text


class ChatGPT:
    """
    OpenAI ChatGPT API wrapper
    """

    _openai: openai
    temperature: float

    def __init__(self):
        self._openai = openai
        self._openai.api_key = os.environ["OPENAI_API_KEY"]

    def answer(self, history: list):
        response = self._openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=history,
            temperature=self.temperature,
        )
        response_text = response["choices"][0]["message"]["content"].strip()
        logging.info(f"[OpenAI] response: {response_text}")
        return response_text
