import json
import logging
import os

import requests


class WecomApp:
    access_token: str
    corp_id: str
    secret: str
    message: str
    userid: str

    def __init__(self, message: str, userid: str = "@all"):
        self.base_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
        self.access_token = ""
        self.agent_id = ""
        self.message = message
        self.userid = userid
        self.get_credential()

    def compose_message(self) -> str:
        msg = {
            "touser": self.userid,
            "msgtype": "text",
            "agentid": self.agent_id,
            "text": {"content": self.message},
            "safe": 0,
        }
        return json.dumps(msg)

    def send(self) -> [bool, str]:
        msg = self.compose_message()
        url = f"{self.base_url}{self.access_token}"
        rs = requests.post(
            url,
            data=msg,
            headers={"Content-Type": "application/json"},
        )
        rs = json.loads(rs.text)
        logging.info(f"Message sent to wecom: {rs['errmsg']}")
        if rs["errcode"] == 0:
            return True, rs["errmsg"]
        return False, rs["errmsg"]

    def get_credential(self):
        self.secret = os.environ["WECOM_SECRET"]
        self.agent_id = os.environ["WECOM_AGENT_ID"]
        self.corp_id = os.environ["WECOM_CORP_ID"]

        auth_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corp_id}&corpsecret={self.secret}"
        rs = requests.get(auth_url)
        rs = json.loads(rs.text)
        if rs["errcode"] == 0:
            self.access_token = rs["access_token"]
        else:
            logging.error(f"Failed to get access token: {rs['errmsg']}")
            raise WecomAppMessageException(
                f"Failed to get access token: {rs['errmsg']}"
            )


class WecomAppMessageException(Exception):
    pass
