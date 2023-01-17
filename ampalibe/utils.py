import os
import sys
import json
import requests
from .payload import Payload
from conf import Configuration  # type: ignore


LANGS = None


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
    this function uses the langs.json file.
    translate a keyword or sentence
    """
    global LANGS

    if not lang:
        return key

    if not os.path.isfile("langs.json"):
        print("Warning! langs.json not found", file=sys.stderr)
        from .source import langs

        with open("langs.json", "w", encoding="utf-8") as lang_file:
            lang_file.write(langs)
            print("langs.json created!")
        return key

    if not LANGS:
        with open("langs.json", encoding="utf-8") as lang_file:
            LANGS = json.load(lang_file)

    keyword = LANGS.get(key)

    if keyword:
        if keyword.get(lang):
            return keyword.get(lang)
    return key


def simulate(sender_id, text, **params):
    """
    Simulate a message send by an user

    Args:
        sender_id: <str>
        text: <str> |<Payload>
    """
    if isinstance(text, Payload):
        text = Payload.trt_payload_out(text)

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
        f"http://127.0.0.1:{Configuration.APP_PORT}/",
        json=data_json,
        headers=header,
        params=params,
    )
