import os
import json
import requests
from retry import retry
import requests_toolbelt


class Analyse:
    def __init__(self, res) -> None:
        if res.status_code != 200:
            print(res.status_code, res.text)


class Messenger:
    def __init__(self, access_token):
        self.token = access_token
        self.url = "https://graph.facebook.com/v8.0/me"

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_message(self, dest_id, message, prio=False):

        self.send_action(dest_id, 'typing_on')
        """
            Cette fonction sert à envoyer une message texte
                à un utilisateur donnée
                                                                """
        data_json = {
            'recipient': {
                "id": dest_id
            },
            'message': {
                "text": message
            }
        }

        if prio:
            data_json["messaging_type"] = "MESSAGE_TAG"
            data_json["tag"] = "ACCOUNT_UPDATE"

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        res = requests.post(
            self.url + '/messages',
            json=data_json,
            headers=header,
            params=params
        )
        self.send_action(dest_id, 'typing_off')
        Analyse(res)
        return res

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_action(self, dest_id, action):
        """
            Cette fonction sert à simuler un action sur les messages.
            exemple: vue, en train d'ecrire.
            Action dispo: ['mark_seen', 'typing_on', 'typing_off']
        """
        data_json = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": dest_id
            },
            'sender_action': action
        }

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        res = requests.post(
            self.url + '/messages',
            json=data_json,
            headers=header,
            params=params
        )
        Analyse(res)
        return res

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_quick_reply(self, dest_id, quick_rep, text):
        '''
            Envoie des quick reply messenger
        '''
        data_json = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": dest_id
            },

            'message': {
                'text': text,
                'quick_replies': quick_rep[:13]
            }
        }

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        res = requests.post(
            self.url + '/messages',
            json=data_json,
            headers=header,
            params=params
        )
        Analyse(res)
        return res

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_result(self, destId, elements, **kwargs):
        '''
            Affichage de resultat de façon structuré
            chez l'utilisateur
        '''
        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": destId
            },
            'message': {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements,
                    },
                },
            }
        }

        if kwargs.get("next"):
            dataJSON['message']['quick_replies'] = kwargs.get("next")

        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}

        res = requests.post(
            self.url + '/messages', json=dataJSON,
            headers=header, params=params
        )
        Analyse(res)
        return res

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_file_url(self, destId, url, filetype='file'):
        '''
            Envoyé piece jointe par lien.
        '''

        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": destId
            },
            'message': {
                'attachment': {
                    'type': filetype,
                    'payload': {
                        "url": url,
                        "is_reusable": True
                    }
                }
            }
        }
        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}
        res = requests.post(
            self.url + '/messages',
            json=dataJSON,
            headers=header,
            params=params
        )
        Analyse(res)
        return res

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def persistent_menu(self, destId, persistent_menu, action='PUT'):
        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}
        if action == "PUT":
            dataJSON = {
                "psid": destId,
                persistent_menu: persistent_menu
                # "persistent_menu": [
                #         {
                #             "locale": "default",
                #             "composer_input_disabled": False,
                #             "call_to_actions": [
                #                 {
                #                     "type": "postback",
                #                     "title": '🔎🤖 BOT',
                #                     "payload": "_SHOW_MENU_BOT"
                #                 },
                #                 {
                #                     "type": "postback",
                #                     "title": '👨‍🎓📚 Moodle',
                #                     "payload": "_SHOW_MENU_MOODLE"
                #                 },
                #                 {
                #                     "type": "postback",
                #                     "title": '🚶‍♂️🚶‍♂' +
                #                     translate('liberer', lang),
                #                     "payload": "_CANCEL_ACTION"
                #                 }
                #             ]
                #         }
                #     ]
            }

            res = requests.post(
                self.url + '/custom_user_settings',
                json=dataJSON, headers=header, params=params
            )
            Analyse(res)
            return res

        elif action == "DELETE":
            params['params'] = "(persistent_menu)"
            params['psid'] = destId

            res = requests.delete(
                self.url + '/custom_user_settings',
                headers=header, params=params
            )
            Analyse(res)
            return res

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_file(self, destId, file, filetype="file", filename_=None):
        if filename_ is None:
            filename_ = file
        params = {
             "access_token": self.token
        }

        data = {
            'recipient': json.dumps({'id': destId}),

            'message': json.dumps({
                'attachment': {
                    'type': filetype,
                    'payload': {
                        "is_reusable": True,
                    }
                }
            }),

            'filedata': (
                os.path.basename(filename_),
                open(f'data/{destId}/{file}', 'rb'),
                f"{filetype}/{file.split('.')[-1]}"
            )
        }

        # multipart encode the entire payload
        multipart_data = requests_toolbelt.MultipartEncoder(data)

        # multipart header from multipart_data
        header = {
            'Content-Type': multipart_data.content_type
        }

        res = requests.post(
            self.url + '/messages',
            params=params, headers=header, data=multipart_data
        )
        Analyse(res)
        return res
