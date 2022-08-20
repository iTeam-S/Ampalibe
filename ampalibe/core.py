import os
import sys
import pickle
import asyncio
import uvicorn
from .model import Model
from threading import Thread
from conf import Configuration  # type: ignore
from .messenger import Messenger
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Response
from .utils import funcs, analyse, Cmd, Payload

_req = None
loop = None

webserver = FastAPI(title="Ampalibe server")
if os.path.isdir("assets/public"):
    webserver.mount("/asset", StaticFiles(directory="assets/public"), name="asset")


class Extra:
    def __init__(self, *args):
        self.query = Model()
        self.chat = Messenger()

    @staticmethod
    def run():
        """
        function that run framework
        """
        global _req
        _req = Model()

        global loop
        loop = asyncio.get_event_loop()
        Thread(target=loop.run_forever).start()

        uvicorn.run(
            "ampalibe:webserver",
            port=Configuration.APP_PORT,
            host=Configuration.APP_HOST,
        )


class Server:
    """
    Content of webhook
    """

    @webserver.on_event("shutdown")
    def shutdow():
        """
        function that shutdown crontab server
        """
        loop.call_soon_threadsafe(loop.stop)

    @webserver.get("/")
    async def verif(request: Request):
        """
        Main verification for bot server is received here
        """
        fb_token = request.query_params.get("hub.verify_token")

        if fb_token == Configuration.VERIF_TOKEN:
            return Response(content=request.query_params["hub.challenge"])
        return "Failed to verify token"

    @webserver.post("/")
    async def main(request: Request):
        """
        Main Requests for bot messenger is received here.
        """
        testmode = request.query_params.get("testmode")
        data = await request.json()

        # data analysis and decomposition
        sender_id, payload, message = analyse(data)

        if payload.webhook not in ("message", "postback"):
            if funcs["event"].get(payload.webhook):
                kw = {"sender_id": sender_id, "watermark": payload, "message": message}
                if testmode:
                    funcs["event"][payload.webhook](**kw)
                else:
                    Thread(target=funcs["event"][payload.webhook], kwargs=kw).start()
            return {"status": "ok"}

        _req._verif_user(sender_id)
        # get action for the current user
        action = _req.get_action(sender_id)
        lang = _req.get_lang(sender_id)

        if payload in ("/__next", "/__more"):
            bot = Messenger()
            if os.path.isfile(f"assets/private/.__{sender_id}"):
                elements = pickle.load(open(f"assets/private/.__{sender_id}", "rb"))
                if payload == "/__next":
                    bot.send_template(sender_id, elements[0], next=elements[1])
                else:
                    bot.send_quick_reply(
                        sender_id, elements[0], elements[1], next=elements[2]
                    )
                return {"status": "ok"}

        if os.path.isfile(f"assets/private/.__{sender_id}"):
            os.remove(f"assets/private/.__{sender_id}")

        payload, kw = Payload.trt_payload_in(payload)
        command = funcs["command"].get(payload.split()[0])
        kw["sender_id"] = sender_id
        kw["cmd"] = payload
        kw["message"] = message
        kw["lang"] = lang
        if command:
            _req.set_action(sender_id, None)
            if testmode:
                return command(**kw)
            else:
                Thread(
                    target=command,
                    kwargs=kw,
                ).start()
        elif action and funcs["action"].get(action):
            """
            CASE an action is set.
            """
            if testmode:
                return funcs["action"].get(action)(**kw)
            Thread(target=funcs["action"].get(action), kwargs=kw).start()
        else:
            command = funcs["command"].get("/")
            if action:
                print(
                    f'\033[48:5:166m⚠ Warning!\033[0m action "{action}" undeclared',
                    file=sys.stderr,
                )
            if command:
                if testmode:
                    return command(**kw)
                Thread(target=command, kwargs=kw).start()
            else:
                print(
                    "\033[31mError! \033[0mDefault route '/' function undeclared.",
                    file=sys.stderr,
                )
        return {"status": "ok"}
