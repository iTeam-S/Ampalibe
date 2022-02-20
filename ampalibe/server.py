
import uvicorn
from typing import Dict
from threading import Thread
from .utils import analyse, funcs
from .requete import Request as Model
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Response

_req = None
conf = None
webserver = FastAPI()
webserver.mount("/asset", StaticFiles(directory="assets/public"), name="asset")


def req(cnf):
    return Model(cnf)


def run(cnf):
    '''
        Fonction principale qui 
        demarre le serveur.
    '''
    global conf
    global _req
    conf = cnf
    _req = Model(cnf)
    uvicorn.run(webserver)


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

    if action and funcs['action'].get(action):
            Thread(
                target=funcs['action'].get(action),
                args=(sender_id, payload)
            ).start()
    else:
        Thread(
            target=funcs['commande'].get(payload.split()[0], funcs['commande']['/']),
            args=(sender_id, payload)
        ).start()

    return {'status': 'ok'}
