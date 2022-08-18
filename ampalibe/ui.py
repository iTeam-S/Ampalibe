"""
    List of All UI Widget Messenger 
"""
from .utils import Payload


class QuickReply:
    def __init__(self, **kwargs):
        """
        Object that can be used to generated a quick_reply
        """
        self.content_type = kwargs.get("content_type", "text")
        if self.content_type not in ("text", "user_phone_number", "user_email"):
            raise ValueError(
                "content_type can only be 'text', 'user_phone_number', 'user_email'"
            )

        self.title = kwargs.get("title")
        self.payload = kwargs.get("payload")

        if self.content_type == "text" and not self.payload:
            raise ValueError("payload must be present for text")

        if self.content_type == "text" and not self.title:
            raise ValueError("title must be present for text")

        self.image_url = kwargs.get("image_url")

    @property
    def value(self):
        res = {"content_type": self.content_type}

        if self.content_type == "text":
            res["title"] = self.title

            if self.payload:
                res["payload"] = Payload.trt_payload_out(self.payload)

            if self.image_url:
                res["image_url"] = self.image_url
        return res

    def __str__(self):
        return str(self.value)


class Button:
    def __init__(self, **kwargs):

        self.type = kwargs.get("type", "postback")
        self.title = kwargs.get("title")
        self.url = kwargs.get("url")
        self.payload = kwargs.get("payload")

        if self.type not in (
            "postback",
            "web_url",
            "phone_number",
            "account_link",
            "account_unlink",
        ):
            raise ValueError(
                "type must be one of 'postback', 'web_url', 'phone_number', 'account_link', 'account_unlink'"
            )

        if self.type in ("postback", "phone_number"):

            if not self.payload:
                raise ValueError("payload must be present")

            if not self.title:
                raise ValueError("title must be present")

        elif self.type == "web_url":
            if not self.url:
                raise ValueError("url must be present for web_url")

            if not self.title:
                raise ValueError("title must be present for web_url")

        elif self.type == "account_link":
            if not self.url:
                raise ValueError("url facebook login must be present for account_link")

    @property
    def value(self):
        if self.payload:
            self.payload = Payload.trt_payload_out(self.payload)

        if self.type in ("postback", "phone_number"):
            return {"type": self.type, "title": self.title, "payload": self.payload}

        elif self.type == "web_url":
            return {"type": "web_url", "title": self.title, "url": self.url}

        elif self.type == "account_link":
            return {"type": "account_link", "url": self.url}

        elif self.type == "account_unlink":
            return {"type": "account_unlink"}

    def __str__(self):
        return str(self.value)


class Element:
    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.subtitle = kwargs.get("subtitle")
        self.image = kwargs.get("image_url")
        self.buttons = kwargs.get("buttons")

        if not self.title:
            raise ValueError("Element must be have a title")

        if not self.buttons:
            raise ValueError("Element must be have a buttons")

        if not isinstance(self.buttons, list):
            raise ValueError("buttons must be a list of Button")

        if len(self.buttons) > 3:
            raise ValueError("buttons must be three maximum")

        for i in range(len(self.buttons)):
            if not isinstance(self.buttons[i], Button):
                raise ValueError("buttons must a List of Button")

    @property
    def value(self):
        res = {"title": self.title}

        if self.subtitle:
            res["subtitle"] = self.subtitle

        if self.image:
            res["image_url"] = self.image

        res["buttons"] = [button.value for button in self.buttons]

        return res

    def __str__(self):
        return str(self.value)
