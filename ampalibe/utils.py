funcs = {'commande': {}, 'action': {}}

def analyse(data):
    '''
        Fonction analysant les données reçu de Facebook
        Donnée de type Dictionnaire attendu (JSON parsé)
    '''
    def struct_atts(data):
        return data['payload']['url']

    for event in data['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                # recuperation de l'id de l'utilisateur
                sender_id = message['sender']['id']
                if message['message'].get('attachments'):
                    # recuperations des fichiers envoyés.
                    data = message['message'].get('attachments')
                    return sender_id, ','.join(list(map(struct_atts, data)))
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

def command(*args, **kwargs):
    def call_fn(function):
        funcs['commande'][args[0]] = function
    return call_fn

def action(*args, **kwargs):
    def call_fn(function):
        funcs['action'][args[0]] = function
    return call_fn
