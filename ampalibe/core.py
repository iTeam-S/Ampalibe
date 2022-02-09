
import uvicorn
from typing import Dict
from fastapi import FastAPI

funcs = {}
webserver = FastAPI()

def commande(*args, **kwargs):
    def call_fn(function):
        funcs[args[0]] = function
    return call_fn

def run():
    uvicorn.run(webserver)

@webserver.get('/{payload}')
async def main(payload) -> Dict:
    init = '/'
    func = funcs.get(init + payload)
    if func:
        func(user_id="user_test", message='test')
    else:  # ato rehefa tsy hitany de alefa amn func par defaut
        funcs[init](user_id="user_test", message='test')
    return {'status': 'ok'}
