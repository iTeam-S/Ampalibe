import urllib.parse


funcs = {'commande': {}, 'action': {}}


class Payload:
    '''
        Object for Payload Management
    '''
    def __init__(self, payload, **kwargs) -> None:
        '''
            Object for Payload Management
        '''
        self.payload = payload
        self.data = kwargs

    @staticmethod
    def trt_payload_in(payload):
        """
        processing of payloads received in a sequence of structured parameters
        
        @params: payload [String]
        @return: payload [String] , structured parameters Dict
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

    @staticmethod
    def trt_payload_out(payload):
        """
        Processing of a Payload type as a character string
        
        @params: payload [ Payload | String ]
        @return: String
        """
        if isinstance(payload, Payload):
            tmp = ''
            for key_data, val_data in payload.data.items():
                tmp += f'{{{{{key_data}==={val_data}}}}} '
            return urllib.parse.quote(payload.payload + ' ' + tmp)
        return urllib.parse.quote(payload)


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
                    return sender_id, ','.join(list(map(struct_atts, data))), message
                elif message['message'].get('quick_reply'):
                    # if the response is a quick reply
                    return  sender_id, message['message']['quick_reply'].get('payload'), message
                elif message['message'].get('text'):
                    # if the response is a simple text
                    return  sender_id, message['message'].get('text'), message
            if message.get('postback'):
                recipient_id = message['sender']['id']
                pst_payload = message['postback']['payload']
                return recipient_id, pst_payload, message


def command(*args, **kwargs):
    """
        A decorator that registers the function as the route 
            of a processing per command sent.
    """
    def call_fn(function):
        funcs['commande'][args[0]] = function
    return call_fn


def action(*args, **kwargs):
    """
        A decorator that registers the function as the route
            of a defined action handler.
    """
    def call_fn(function):
        funcs['action'][args[0]] = function
    return call_fn
