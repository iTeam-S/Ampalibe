
import uvicorn
from typing import Dict
from os import getenv as env
from threading import Thread
from fastapi import FastAPI, Request, Response

funcs = {}
webserver = FastAPI()

def commande(*args, **kwargs):
    def call_fn(function):
        funcs[args[0]] = function
    return call_fn

def run():
    uvicorn.run(webserver)

def analyse(data):
    '''
        Fonction analysant les données reçu de Facebook
        Donnée de type Dictionnaire attendu (JSON parsé)
    '''
    for event in data['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                # recuperation de l'id de l'utilisateur
                sender_id = message['sender']['id']
                if message['message'].get('attachments'):
                    # recuperations des fichiers envoyés.
                    data = message['message'].get('attachments')
                    # data[0]['type'] == 'file'
                    return sender_id, data[0]['payload']['url']
                elif message['message'].get('attachments'):
                    # recuperations des fichiers envoyés.
                    data = message['message'].get('attachments')
                    # data[0]['type'] == 'file'
                    return  sender_id, data[0]['payload']['url']
                elif message['message'].get('quick_reply'):
                    # cas d'une reponse de type QUICK_REPLY
                    return  sender_id, message['message']['quick_reply'].get('payload')
                elif message['message'].get('text'):
                    # cas d'une reponse par text simple.
                    return  sender_id, message['message'].get('text')
            if message.get('postback'):
                recipient_id = message['sender']['id']
                pst_payload = message['postback']['payload']
                return recipient_id, pst_payload


@webserver.get('/')
async def verif(request: Request) -> Dict:
    fb_token = request.query_params.get("hub.verify_token")

    if fb_token == env("AMP_VERIF_TOKEN"):
        return Response(content=request.query_params["hub.challenge"])
    return 'Failed to verify token'


@webserver.post('/')
async def main(request: Request) -> Dict:
    data = await request.json()
    sender_id, payload = analyse(data)
    Thread(target=funcs.get(payload, funcs['/']), args=(sender_id, payload)).start()

    return {'status': 'ok'}
