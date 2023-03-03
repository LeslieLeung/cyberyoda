from cyberyoda.bot.history.history import ChatHistory
from cyberyoda.sdk.openai.api import ChatGPT
from cyberyoda.sdk.wecom.app_message import WecomApp
from cyberyoda.storage.mongo import Mongo


def handle_chat(prompt: str, userid: str):
    openai = ChatGPT()
    prompt = prompt.replace("/chat", "").strip()
    chat_history = ChatHistory(Mongo(), userid=userid)
    chat_history.log_user(prompt)
    resp = openai.answer(chat_history.history)
    chat_history.log_assistant(resp)
    chat_history.save()
    wecom = WecomApp(resp, userid=userid)
    wecom.send()


def handle_reset(userid: str):
    chat_history = ChatHistory(Mongo(), userid=userid)
    chat_history.reset()
    return "[System] Chat history has been reset."


def handle_system(prompt: str, userid: str):
    chat_history = ChatHistory(Mongo(), userid=userid)
    prompt = prompt.replace("/system", "").strip()
    chat_history.add("system", prompt)
    chat_history.save()
    return "[System] Instruction has been saved."
