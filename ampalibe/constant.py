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
