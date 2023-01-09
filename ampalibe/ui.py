"""
    List of All UI Widget Messenger 
"""
from .payload import Payload
from .constant import (
    Type,
    Content_type,
    Notification_reoptin,
    Notification_cta_text,
    Notification_frequency,
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
        self.default_action = kwargs.get("default_action")

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

        if self.default_action:
            if not isinstance(self.default_action, Button):
                raise ValueError("default_action must be a Button")

    @property
    def value(self):
        res = {"title": self.title}

        if self.subtitle:
            res["subtitle"] = self.subtitle

        if self.image:
            res["image_url"] = self.image

        if self.default_action:
            res["default_action"] = self.default_action.value

        res["buttons"] = [button.value for button in self.buttons]  # type: ignore

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


class RecurringNotificationOptin:
    def __init__(self, **kwargs):
        """
        RecurringNotificationOptin ui object to be used in the send_optin
        Args:
            title (str) - Title of the optin
            image (str | optional) - Image url of the optin
            payload (str) - Payload of the optin
            notification_frequency (str) - Frequency of the notification messages
        """
        self.template_type = "notification_messages"
        self.title = kwargs.get("title")
        self.image_url = kwargs.get("image_url")
        self.payload = kwargs.get("payload")
        self.notification_frequency = kwargs.get("notification_frequency")
        self.notification_cta_text = kwargs.get("notification_cta_text")
        self.notification_reoptin = kwargs.get("notification_reoptin")

        if not self.title:
            raise ValueError("RecurringNotificationOptin must have a title")

        if not self.payload:
            raise ValueError("RecurringNotificationOptin must have a payload")

        if not self.notification_frequency:
            raise ValueError(
                "RecurringNotificationOptin must have a notification frequency"
            )

        if self.notification_frequency not in Notification_frequency:
            raise ValueError(
                "RecurringNotificationOptin must have a valid notification frequency"
            )

        if self.notification_cta_text:
            if self.notification_cta_text not in Notification_cta_text:
                raise ValueError(
                    "RecurringNotificationOptin must have a valid notification cta text"
                )

        if self.notification_reoptin:
            if self.notification_reoptin not in Notification_reoptin:
                raise ValueError(
                    "RecurringNotificationOptin must have a valid notification reoptin"
                )

    @property
    def value(self):
        res = {
            "template_type": self.template_type,
            "title": self.title,
            "notification_messages_frequency": self.notification_frequency.value,  # type: ignore
        }

        if isinstance(self.payload, Payload):
            res["payload"] = Payload.trt_payload_out(self.payload)
        else:
            res["payload"] = self.payload

        if self.image_url:
            res["image_url"] = self.image_url

        if self.notification_cta_text:
            res["notification_messages_cta_text"] = self.notification_cta_text.value

        if self.notification_reoptin:
            res["notification_messages_reoptin"] = self.notification_reoptin.value

        return res

    def __str__(self):
        return str(self.value)


class Product:
    def __init__(self, id):
        self.id = id

    @property
    def value(self):
        return {"id": self.id}

    def __str__(self):
        return str(self.value)
