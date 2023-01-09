from .tools import funcs


def command(*args, **kwargs):
    """
    A decorator that registers the function as the route
        of a processing per command sent.
    """

    def call_fn(function):
        funcs["command"][args[0]] = function

    return call_fn


def action(*args, **kwargs):
    """
    A decorator that registers the function as the route
        of a defined action handler.
    """

    def call_fn(function):
        funcs["action"][args[0]] = function

    return call_fn


def event(*args, **kwargs):
    """
    A decorator that registers the function as the route
        of a defined event handler.
    """

    def call_fn(function):
        funcs["event"][args[0]] = function

    return call_fn


def before_receive(*args, **kwargs):
    """
    A decorator that run the function before
        running apropriate function
    """

    def call_fn(function):
        funcs["before"] = function

    return call_fn


def after_receive(*args, **kwargs):
    """
    A decorator that run the function after
        running apropriate function
    """

    def call_fn(function):
        funcs["after"] = function

    return call_fn
