import os
import sys
import json
import requests
from .custom_cmd import Cmd
from conf import Configuration  # type: ignore


funcs = {
    "command": {},
    "action": {},
    "event": {},
    "before": None,
    "after": None,
}


def analyse(data):
    """
    Function analyzing data received from Facebook
    The data received are of type Json .
    """

    def struct_atts(data):
        return data["payload"]["url"]

    for event in data["entry"]:
        messaging = event["messaging"]

        for message in messaging:

            sender_id = message["sender"]["id"]

            if message.get("message"):

                if message["message"].get("attachments"):
                    # Get file name
                    data = message["message"].get("attachments")
                    # creation de l'objet cmd personalisé
                    atts = list(map(struct_atts, data))
                    cmd = Cmd(atts[0])
                    cmd.set_atts(atts)
                    cmd.webhook = "attachments"
                    return sender_id, cmd, message
                elif message["message"].get("quick_reply"):
                    # if the response is a quick reply
                    return (
                        sender_id,
                        Cmd(message["message"]["quick_reply"].get("payload")),
                        message,
                    )
                elif message["message"].get("text"):
                    # if the response is a simple text
                    return (
                        sender_id,
                        Cmd(message["message"].get("text")),
                        message,
                    )

            if message.get("postback"):
                recipient_id = sender_id
                pst_payload = Cmd(message["postback"]["payload"])
                pst_payload.webhook = "postback"
                return recipient_id, pst_payload, message

            if message.get("read"):
                watermark = Cmd(message["read"]["watermark"])
                watermark.webhook = "read"
                return sender_id, watermark, message

            if message.get("delivery"):
                watermark = Cmd(message["delivery"]["watermark"])
                watermark.webhook = "delivery"
                return sender_id, watermark, message

            if message.get("reaction"):
                reaction = Cmd(message["reaction"]["reaction"])
                reaction.webhook = message["reaction"]["action"]
                return sender_id, reaction, message


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


def download_file(url, file):
    """
    Downloading a file from an url.

    Args:
        url: direct link for the attachment

        file: filename with path
    """
    res = requests.get(url, allow_redirects=True)

    with open(file, "wb") as f:
        f.write(res.content)

    return file


def translate(key, lang):
    """
    translate a keyword or sentence

    @params:

        key: the key used in langs.json file

        lang: the langage code in format fr, en, mg, ...

    this function uses the langs.json file.
    """
    if not lang:
        return key

    if not os.path.isfile("langs.json"):
        print("Warning! langs.json not found", file=sys.stderr)
        from .source import langs

        with open("langs.json", "w") as fichier:
            fichier.write(langs)
            print("langs.json created!")
        return key

    with open("langs.json") as fichier:
        trans = json.load(fichier)

    keyword = trans.get(key)

    if keyword:
        if keyword.get(lang):
            return keyword.get(lang)
    return key


def simulate(sender_id, text, **params):
    """
    Simulate a message send by an user
    """
    data_json = {
        "object": "page",
        "entry": [
            {
                "messaging": [
                    {
                        "message": {
                            "text": text,
                        },
                        "sender": {"id": sender_id},
                    }
                ]
            }
        ],
    }
    header = {"content-type": "application/json; charset=utf-8"}
    return requests.post(
        f"http://127.0.0.1:{Configuration.APP_PORT}",
        json=data_json,
        headers=header,
        params=params,
    )


def before_run(func, **kwargs):
    res = None
    if funcs["before"] and hasattr(funcs["before"], "__call__"):
        if funcs["before"](**kwargs):
            res = func(**kwargs)
    else:
        res = func(**kwargs)

    if funcs["after"] and hasattr(funcs["after"], "__call__"):
        kwargs["res"] = res
        funcs["after"](**kwargs)

    return res
