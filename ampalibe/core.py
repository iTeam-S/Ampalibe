import os
import json
import asyncio
import uvicorn
from .model import Model
from .logger import Logger
from threading import Thread
from .payload import Payload
from conf import Configuration  # type: ignore
from .messenger import Messenger
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Response
from .tools import funcs, analyse, before_run, send_next, verif_event

_req = Model(init=False)
loop = asyncio.get_event_loop()

webserver = FastAPI(title="Ampalibe server")
if not os.path.isdir("assets/public"):
    os.makedirs("assets/public", exist_ok=True)

webserver.mount("/asset", StaticFiles(directory="assets/public"), name="asset")


class Init:
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

        Thread(target=loop.run_forever).start()

        uvicorn.run(
            "ampalibe:webserver",
            port=Configuration.APP_PORT,
            host=Configuration.APP_HOST,
        )


class Server(Request):
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

        if request.query_params.get("hub.verify_token") == Configuration.VERIF_TOKEN:
            return Response(content=request.query_params["hub.challenge"])
        return "Failed to verify token"

    @webserver.post("/")
    async def main(request: Request):
        """
        Main Requests for bot messenger is received here.
        """
        testmode = request.query_params.get("testmode")
        try:
            data = await request.json()
        except json.decoder.JSONDecodeError:
            return "..."

        # data analysis and decomposition
        sender_id, payload, message = analyse(data)

        if payload.webhook in ("read", "delivery", "reaction"):
            verif_event(sender_id, payload, message, testmode)
            return {"status": "ok"}

        _req._verif_user(sender_id)
        action, lang = _req.get(sender_id, "action", "lang")

        if payload in ("/__next", "/__more"):
            send_next(sender_id, payload)
            return {"status": "ok"}

        if os.path.isfile(f"assets/private/.__{sender_id}"):
            os.remove(f"assets/private/.__{sender_id}")

        payload, kw = Payload.trt_payload_in(payload)
        kw.update(
            {
                "sender_id": sender_id,
                "cmd": payload,
                "message": message,
                "lang": lang,
            }
        )

        command = funcs["command"].get(payload.split()[0])

        if command:
            _req.set_action(sender_id, None)
            if testmode:
                return before_run(command, **kw)
            else:
                Thread(
                    target=before_run,
                    args=(command,),
                    kwargs=kw,
                ).start()
        elif action:
            action, kw_tmp = Payload.trt_payload_in(action)
            kw.update(kw_tmp)

            if funcs["action"].get(action):
                if testmode:
                    return before_run(funcs["action"].get(action), **kw)
                Thread(
                    target=before_run,
                    args=(funcs["action"].get(action),),
                    kwargs=kw,
                ).start()
            else:
                Logger.error(f'⚠ Error! action "{action}" undeclared ')
        else:
            command = funcs["command"].get("/")
            if command:
                if testmode:
                    return before_run(command, **kw)
                Thread(target=before_run, args=(command,), kwargs=kw).start()
            else:
                Logger.error("⚠ Error! Default route '/' function undeclared.")
        return {"status": "ok"}
