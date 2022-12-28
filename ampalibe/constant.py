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


class Message_frequency:
    @property
    def DAILY(self):
        """
        subscribe to receive a notification every twenty-four hours for 6 months
        """
        return "DAILY"

    @property
    def WEEKLY(self):
        """
        subscribe to receive a notification every 7 days for 9 months.
        """
        return "WEEKLY"

    @property
    def MONTHLY(self):
        """
        subscribe to receive a notification every month for 12 months.
        """
        return "MONTHLY"


class Notification_messages_cta_text:
    @property
    def ALLOW(self):
        """
        Sets the subscribe message button text to "Allow Messages".
        """
        return "ALLOW"

    @property
    def FREQUENCY(self):
        """
        Sets the text of the subscription message button to "Get messages [daily/weekly/monthly]".
        """
        return "FREQUENCY"

    @property
    def GET(self):
        """
        GET: Sets the subscribe message button text to "Receive messages". This is the default if notif_messages_cta_text is not set.
        """
        return "GET"

    @property
    def OPT_IN(self):
        """
        OPT_IN: Sets the subscribe message button text to "Subscribe to messages".
        """
        return "OPT_IN"

    @property
    def SIGN_UP(self):
        """
        Sets the subscribe message button text to "Sign up for messages".
        """
        return "SIGN_UP"
