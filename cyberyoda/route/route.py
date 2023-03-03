import os
from xml.etree.ElementTree import fromstring

from fastapi import BackgroundTasks, FastAPI, Request, Response

from cyberyoda.bot import handle_chat, handle_func
from cyberyoda.sdk.wecom.encrypt import WXBizMsgCrypt


def register_route(app: FastAPI):
    token = os.environ["WECOM_TOKEN"]
    aeskey = os.environ["WECOM_AESKEY"]
    corp_id = os.environ["WECOM_CORP_ID"]
    wxcpt = WXBizMsgCrypt(token, aeskey, corp_id)

    @app.get("/")
    async def verify(msg_signature: str, timestamp: str, nonce: str, echostr: str):
        ret, s_echo_str = wxcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)
        if ret == 0:
            return Response(content=s_echo_str.decode("utf-8"))
        else:
            print(s_echo_str)
        return echostr

    @app.post("/")
    async def receive(
        request: Request,
        msg_signature: str,
        timestamp: str,
        nonce: str,
        background_tasks: BackgroundTasks,
    ):
        body = await request.body()
        ret, s_msg = wxcpt.DecryptMsg(
            body.decode("utf-8"), msg_signature, timestamp, nonce
        )
        decrypt_data = {}
        for node in list(fromstring(s_msg.decode("utf-8"))):
            decrypt_data[node.tag] = node.text

        if decrypt_data["Content"].startswith("/"):
            resp = handle_func(decrypt_data)
            ret, send_msg = wxcpt.EncryptMsg(sReplyMsg=resp, sNonce=nonce)
            if ret == 0:
                return Response(content=send_msg)
        background_tasks.add_task(
            handle_chat, decrypt_data["Content"], decrypt_data["FromUserName"]
        )
        return Response(content="")
