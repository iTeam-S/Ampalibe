from enum import Enum


class Content_type:
    text = "text"
    user_phone_number = "user_phone_number"
    user_email = "user_email"


class Type:
    postback = "postback"
    web_url = "web_url"
    phone_number = "phone_number"
    account_link = "account_link"
    account_unlink = "account_unlink"


class Notification_frequency(Enum):
    """
    Message frequency for the subscription message.
    """

    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"


class Notification_cta_text(Enum):
    """
    Call to action text for the subscription message.
    """

    ALLOW = "ALLOW"
    FREQUENCY = "FREQUENCY"
    GET = "GET"
    OPT_IN = "OPT_IN"
    SIGN_UP = "SIGN_UP"


class Notification_reoptin(Enum):
    """
    Reoptin action for the subscription message.
    """

    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class Action:
    mark_seen = "mark_seen"
    typing_on = "typing_on"
    typing_off = "typing_off"


class Filetype:
    file = "file"
    video = "video"
    image = "image"
    audio = "audio"


class Messaging_type:
    MESSAGE_TAG = "MESSAGE_TAG"
    RESPONSE = "RESPONSE"
    UPDATE = "UPDATE"


class Tag:
    ACCOUNT_UPDATE = "ACCOUNT_UPDATE"
    CONFIRMED_EVENT_UPDATE = "CONFIRMED_EVENT_UPDATE"
    CUSTOMER_FEEDBACK = "CUSTOMER_FEEDBACK"
    HUMAN_AGENT = "HUMAN_AGENT"
    POST_PURCHASE_UPDATE = "POST_PURCHASE_UPDATE"


class Notification_type:
    NO_PUSH = "NO_PUSH"
    REGULAR = "REGULAR"
    SILENT_PUSH = "SILENT_PUSH"
