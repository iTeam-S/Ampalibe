"""
    List of All UI Widget Messenger 
"""
from .payload import Payload
from .constant import (
    Content_type,
    Type,
    Message_frequency,
    Notification_messages_cta_text,
)


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


class ReceiptElement:
    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.subtitle = kwargs.get("subtitle")
        self.quantity = kwargs.get("quantity")
        self.price = kwargs.get("price")
        self.currency = kwargs.get("currency")
        self.image = kwargs.get("image_url")

        if not self.title:
            raise ValueError("Receipt element must be have a title")

        if not self.price:
            raise ValueError("Receipt element must be have a price")

    @property
    def value(self):
        res = {"title": self.title}

        if self.subtitle:
            res["subtitle"] = self.subtitle

        if self.quantity:
            res["quantity"] = self.quantity

        res["price"] = self.price
        res["currency"] = self.currency

        if self.image:
            res["image_url"] = self.image

        return res

    def __str__(self):
        return str(self.value)


class Summary:
    def __init__(self, **kwargs):
        self.subtotal = kwargs.get("subtotal")
        self.shipping_cost = kwargs.get("shipping_cost")
        self.total_tax = kwargs.get("total_tax")
        self.total_cost = kwargs.get("total_cost")

        if not self.total_cost:
            raise ValueError("Summary must have a total_cost")

    @property
    def value(self):
        res = {"total_cost": self.total_cost}

        if self.shipping_cost:
            res["shipping_cost"] = self.shipping_cost

        if self.total_tax:
            res["total_tax"] = self.total_tax

        if self.subtotal:
            res["subtotal"] = self.subtotal

        return res

    def __str__(self):
        return str(self.value)


class Address:
    def __init__(self, **kwargs):
        self.street_1 = kwargs.get("street_1")
        self.street_2 = kwargs.get("street_2")
        self.city = kwargs.get("city")
        self.postal_code = kwargs.get("postal_code")
        self.state = kwargs.get("state")
        self.country = kwargs.get("country")

        if not self.street_1:
            raise ValueError("Address must have a street_1")

        if not self.city:
            raise ValueError("Address must have a city")

        if not self.postal_code:
            raise ValueError("Address must have a postal_code")

        if not self.state:
            raise ValueError("Address must have a state")

        if not self.country:
            raise ValueError("Address must have a country")

    @property
    def value(self):
        res = {}

        if self.street_1:
            res["street_1"] = self.street_1

        if self.street_2:
            res["street_2"] = self.street_2

        if self.city:
            res["city"] = self.city

        if self.postal_code:
            res["postal_code"] = self.postal_code

        if self.state:
            res["state"] = self.state

        if self.country:
            res["country"] = self.country

        return res

    def __str__(self):
        return str(self.value)


class Adjustment:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.amount = kwargs.get("amount")

        if not self.name:
            raise ValueError("Adjustment must be have a name")

        if not self.amount:
            raise ValueError("Adjustment must be have a amount")

    @property
    def value(self):
        return {"name": self.name, "amount": self.amount}

    def __str__(self):
        return str(self.value)


class RecurringNotification:
    def __init__(self, **kwargs):
        """
            Recurring notification ui object to be used in the send_recurring_notification
            Args:
                title (str) - Title of the notification
                image (str | optional) - Image url of the notification
                payload (str) - Payload of the notification
                notification_messages_frequency (str) - "DAILY" or "WEEKLY" or "MONTHLY"
                notification_messages_cta_text (str) - "GET" or "SIGN_UP" or "ALLOW" or "OPT_IN" or "FREQUENCY"
                image_aspect_ratio (str | optional) - "HORIZONTAL" or "SQUARE"
                notification_reoptin (str | optional) - "ENABLED" or "DISABLED"
        """
        self.template_type = "notification_messages"
        self.title = kwargs.get("title")
        self.image = kwargs.get("image_url")
        self.payload = kwargs.get("payload")
        self.notification_messages_frequency = kwargs.get(
            "notification_messages_frequency"
        )
        self.notification_messages_cta_text = kwargs.get(
            "notification_messages_cta_text"
        )
        self.image_ratio = kwargs.get("image_aspect_ratio")
        self.notification_reoptin = kwargs.get(
            "notification_messages_reoptin"
        )

        if not self.title:
            raise ValueError("Recurring notification must be have a title")

        if not self.payload:
            raise ValueError("Recurring notification must be have a payload")

    @property
    def value(self):
        res = {"template_type": self.template_type, "title": self.title}

        if self.image:
            res["image_url"] = self.image

        if isinstance(self.payload, Payload):
            res["payload"] = Payload.trt_payload_out(self.payload)
        else:
            res["payload"] = self.payload

        if self.notification_messages_frequency:
            res[
                "notification_messages_frequency"
            ] = self.notification_messages_frequency

        if self.notification_messages_cta_text:
            res["notification_messages_cta_text"] = self.notification_messages_cta_text

        return res

    def __str__(self):
        return str(self.value)
