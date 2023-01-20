class Cmd(str):
    """
    Object for text of message
    """

    webhook = "message"
    token = None
    __atts = []

    def __init__(self, text):
        str.__init__(text)

    def set_atts(self, atts):
        for att in atts:
            self.__atts.append(att)

    @property
    def attachments(self):
        return self.__atts

    def copy(self, text):
        new_cmd = Cmd(text)
        new_cmd.__atts = self.attachments
        new_cmd.webhook = self.webhook
        new_cmd.token = self.token
        return new_cmd
