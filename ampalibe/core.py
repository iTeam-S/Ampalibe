import os
import sys
import pickle
import uvicorn
from .requete import Model
from threading import Thread
from .messenger import Messenger
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Response
from .utils import funcs, analyse, Cmd, Payload

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
        # Verif if WORKERS attribute exists
        if hasattr(cnf, 'WORKERS'):
            uvicorn.run('ampalibe:webserver', port=cnf.APP_PORT, host=cnf.APP_HOST, workers=int(cnf.WORKERS))
        else:
            uvicorn.run(webserver, port=cnf.APP_PORT, host=cnf.APP_HOST)


class Server:
    '''
        Content of webhook
    '''

    @webserver.get('/')
    async def verif(request: Request):
        '''
            Main verification for bot server is received here
        '''
        fb_token = request.query_params.get("hub.verify_token")

        if fb_token == conf.VERIF_TOKEN:
            return Response(content=request.query_params["hub.challenge"])
        return 'Failed to verify token'


    @webserver.post('/')
    async def main(request: Request):
        '''
            Main Requests for bot messenger is received here.
        '''
        testmode = request.query_params.get("testmode")
        data = await request.json()

        # data analysis and decomposition
        sender_id, payload, message = analyse(data)
        _req._verif_user(sender_id)
        # get action for the current user
        action = _req.get_action(sender_id)
        lang = _req.get_lang(sender_id)

        if payload in ('/__next', '/__more'):
            bot = Messenger(conf.ACCESS_TOKEN)
            if os.path.isfile(f'assets/private/.__{sender_id}'):
                elements = pickle.load(open(f'assets/private/.__{sender_id}', 'rb'))

                if payload == '/__next':
                    bot.send_template(sender_id, elements[0], next=elements[1])
                else:
                    bot.send_quick_reply(sender_id, elements[0], elements[1], next=elements[2])

                return {'status': 'ok'}

        if os.path.isfile(f'assets/private/.__{sender_id}'):
            os.remove(f'assets/private/.__{sender_id}')

        if action and funcs['action'].get(action):
            '''
                CASE an action is set.
            '''
            kw = {
                'sender_id': sender_id, 'cmd': payload,
                'message': message, 'lang': lang
            }

            if testmode:
                 funcs['action'].get(action)(**kw)
            else:
                Thread(
                    target=funcs['action'].get(action),
                    kwargs=kw
                ).start()
        else:
            if action:
                print(
                    f'Warning! action: "{action}" Not found',
                    file=sys.stderr
                )
            payload, kw = Payload.trt_payload_in(payload)
            kw['sender_id'] = sender_id
            kw['cmd'] = Cmd(payload)  # Remake payload to CMD object
            kw['message'] = message
            kw['lang'] = lang
            if testmode:
                funcs['commande'].get(payload.split()[0], funcs['commande']['/'])(**kw)
            else:
                Thread(
                    target=funcs['commande'].get(payload.split()[0], funcs['commande']['/']),
                    kwargs=kw
                ).start()

        return {'status': 'ok'}
