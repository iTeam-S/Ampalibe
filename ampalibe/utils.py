import urllib.parse

funcs = {'commande': {}, 'action': {}}


class Payload:
    def __init__(self, payload, **kwargs) -> None:
        self.payload = payload
        self.data = kwargs


def analyse(data):
    '''
        Function analyzing data received from Facebook
        The data received are of type Json .
    '''
    def struct_atts(data):
        return data['payload']['url']

    for event in data['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                # Get user_id
                sender_id = message['sender']['id']
                if message['message'].get('attachments'):
                    # Get file name
                    data = message['message'].get('attachments')
                    return sender_id, ','.join(list(map(struct_atts, data)))
                elif message['message'].get('quick_reply'):
                    # if the response is a quick reply
                    return  sender_id, message['message']['quick_reply'].get('payload')
                elif message['message'].get('text'):
                    # if the response is a simple text
                    return  sender_id, message['message'].get('text')
            if message.get('postback'):
                recipient_id = message['sender']['id']
                pst_payload = message['postback']['payload']
                return recipient_id, pst_payload


def command(*args, **kwargs):
    """
    A decorator that will process texts sent by a user from Facebook. 
    This decorator returns the list of functions that the bot must process.
    """
    def call_fn(function):
        funcs['commande'][args[0]] = function
    return call_fn


def action(*args, **kwargs):
    """
    A decorator that will process action of the user in Faebook. 
    This decorator returns the list of functions that the bot must process.
    """
    def call_fn(function):
        funcs['action'][args[0]] = function
    return call_fn


def trt_payload_in(payload):

    """
    A function that will  take as parameter the payload and as output a dictionary .
    example :
        input ==> ({{"id"==="1"}} ,{{"nom"==="user"}})
        output ==> {id= 1,name="user"}
    """

    payload = urllib.parse.unquote(payload)

    res = {}
    while '{{' in payload:
        start = payload.index('{{')
        end = payload.index('}}')
        items = payload[start+2:end].split('===')
        res[items[0]] = items[1]
        payload = payload.replace(payload[start:end+2], '')
    return payload.strip(), res


def trt_payload_out(payload):
    """
    A function that will  take as parameter the object payload and as output a string .
    example :
        input ==> ("etudiant",id=1,name="user")
        output ==> ({{"id"==="1"}},{{"name"==="user"}})
    """
    if isinstance(payload, Payload):
        tmp = ''
        for key_data, val_data in payload.data.items():
            tmp += f'{{{{{key_data}==={val_data}}}}} '
        return urllib.parse.quote(payload.payload + ' ' + tmp)
    return urllib.parse.quote(payload)