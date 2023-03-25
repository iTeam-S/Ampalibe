from .model import Model
from .messenger import Messenger


class Init:
    def __init__(self, *args):
        """
        Leave this class for compatibility with old version
        """
        self.query = Model()
        self.chat = Messenger()
