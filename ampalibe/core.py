import os
import pickle
import uvicorn
from typing import Dict
from threading import Thread
from .messenger import Messenger
from .requete import Request as Model
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Response
from .utils import analyse, funcs, trt_payload_in

_req = None
conf = None
webserver = FastAPI()
if os.path.isdir("assets/public"):
    webserver.mount(
        "/asset",
        StaticFiles(directory="assets/public"),
        name="asset"
    )


class Extra:
    def __init__(self, conf) -> None:
        self.query = Model(conf)
        self.chat = Messenger(conf.ACCESS_TOKEN)

    @staticmethod
    def run(cnf):
        '''
            function that run framework
        '''
        global conf
        global _req
        conf = cnf
        _req = Model(cnf)
        uvicorn.run(webserver, port=cnf.APP_PORT, host=cnf.APP_HOST)


class Server:
    '''
        Content of webhook
    '''
    @webserver.get('/')
    async def verif(request: Request) -> Dict:
        fb_token = request.query_params.get("hub.verify_token")

        if fb_token == conf.VERIF_TOKEN:
            return Response(content=request.query_params["hub.challenge"])
        return 'Failed to verify token'


    @webserver.post('/')
    async def main(request: Request) -> Dict:
        data = await request.json()
        sender_id, payload = analyse(data)
        _req.verif_user(sender_id)
        action = _req.get_action(sender_id)

        if payload == '/__next':
            bot = Messenger(conf.ACCESS_TOKEN)
            if os.path.isfile(f'.__{sender_id}'):
                elements = pickle.load(open(f'.__{sender_id}', 'rb'))
                bot.send_result(sender_id, elements, next=True)
                return {'status': 'ok'}
        try:
            os.remove(f'.__{sender_id}')
        except FileNotFoundError:
            print("ah bon?")

        if action and funcs['action'].get(action):
                Thread(
                    target=funcs['action'].get(action),
                    args=(sender_id, payload)
                ).start()
        else:
            payload, kw = trt_payload_in(payload)
            Thread(
                target=funcs['commande'].get(payload.split()[0], funcs['commande']['/']),
                args=(sender_id, payload),
                kwargs=kw
            ).start()

        return {'status': 'ok'}
