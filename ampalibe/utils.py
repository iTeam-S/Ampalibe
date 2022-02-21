funcs = {'commande': {}, 'action': {}}

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
    def call_fn(function):
        funcs['commande'][args[0]] = function
    return call_fn

def action(*args, **kwargs):
    def call_fn(function):
        funcs['action'][args[0]] = function
    return call_fn
