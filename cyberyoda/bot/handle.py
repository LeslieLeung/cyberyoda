from cyberyoda.bot.handle_chat import handle_reset, handle_system, handle_temp
from cyberyoda.bot.handle_simple import handle_help

resp_template: str = """<xml>
   <ToUserName>{to_username}</ToUserName>
   <FromUserName>{from_username}</FromUserName> 
   <CreateTime>{create_time}</CreateTime>
   <MsgType>text</MsgType>
   <Content>{content}</Content>
</xml>
"""


def handle_func(data: dict):
    prompt = data.get("Content", "")
    userid = data.get("FromUserName")
    match prompt:
        case "/help":
            content = handle_help()
        case "/reset":
            content = handle_reset(userid)
        case s if s.startswith("/system"):
            content = handle_system(prompt, userid)
        case s if s.startswith("/temp"):
            content = handle_temp(prompt, userid)
        case _:
            content = "unknown command"

    return resp_template.format(
        to_username=data.get("FromUserName"),
        from_username=data.get("ToUserName"),
        create_time=data.get("CreateTime"),
        content=content,
    )
