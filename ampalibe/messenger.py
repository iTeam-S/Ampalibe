import os
import json
import requests
from retry import retry
import requests_toolbelt
<<<<<<< Updated upstream
from .utils import trt_payload_out

=======
from requete import Request
import json

req = Request()
>>>>>>> Stashed changes
class Analyse:
    def __init__(self, res) -> None:
        if res.status_code != 200:
            print(res.status_code, res.text)


class Messenger:
    def __init__(self, access_token):
        """
        Here, We need the <access token> of the facebook page we want
        to apply the bot for the purpose of page and bot interaction
        
        Args:
            access_token (str): A facebook page access token
        """
        self.token = access_token
        self.url = "https://graph.facebook.com/v8.0/me"

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_message(self, dest_id, message, prio=False):
        """
        This method sends a message to user given

        Args:
            dest_id (str): user id facebook for the destination
            message (str): message want to send
    
        Returns:
            Response: POST request to the facebook API to send a message to the user
        """
        self.send_action(dest_id, 'typing_on')
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
        This method is used to simulate an action on messages.
        example: view, writing.
        Action available: ['mark_seen', 'typing_on', 'typing_off']

        Args:
            dest_id (str): user id facebook for the destination
            action (str): action ['mark_seen', 'typing_on', 'typing_off']

        Returns:
            Response: POST request to the facebook API to send an action to the user
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
        """
        This is a method to send a <quick_reply>
        to the user

        Args:
            dest_id (str): user id facebook for the destoination
            quick_rep (list of dict): list of the different quick_reply to send a user
            text (str): A text of a little description for each <quick_reply>

        Returns:
            Response: POST request to the facebook API to send a quick_reply to the user
        """

        for i in range(len(quick_rep)):
            quick_rep[i]['payload'] = trt_payload_out(quick_rep[i]['payload'])

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
    def send_result(self, dest_id, elements, **kwargs):
        """
        this method display the result in a structured 
        form at the user(form: template generic),
        
        For this, messenger only validates 10 templates
        for the first display, so we put the optional parameter
        <**kwargs> to manage these numbers if it is a number of 
        elements more than 10,

        So, there is a quick_reply which acts as a "next page"
        displaying all requested templates

        Args:
            dest_id (str): user id facebook for the destination
            elements (list of dict): the list of the specific elements to define the
            structure for the template

        Returns:
            Response: POST request to the facebook API to send a template generic to the user
        """
        
        for i in range(len(elements)):
            for j in range(elements[i]['buttons']):
                elements[i]['buttons'][j]['payload'] = trt_payload_out(elements[i]['buttons'][j]['payload'])

        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": dest_id
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
    def send_file_url(self, dest_id, url, filetype='file'):
        """
        this method sent attachment by link.
        [image,video,pdf,docx,...]
        
        Args:
            dest_id (str): user id facebook for destination
            url (str): the origin url for the file
            filetype (str, optional): type of the file["video","image",...]. Defaults to 'file'.

        Returns:
            Response: POST request to the facebook API to send a template generic to the user
        """

        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient': {
                "id": dest_id
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
    def persistent_menu(self, dest_id, persistent_menu, action='PUT'):
        """
        this is a method to enable a persistent 
        menu for messenger
        
        it sits at the bottom of the screen 
        
        it is not necessarily permanent but we can play
        according to the usefulness, this is why we propose
        the action parameter which is defined its appearance 
        on the screen. we delete it if in an interface or scene
        that we don't need it. we updated it if necessary

        Args:
            dest_id (str): user id for destination
            persistent_menu (list of dict): the elements of the persistent menu to enable
            action (str, optional): the action for benefit["PUT","DELETE"]. Defaults to 'PUT'.
        """
        header = {'content-type': 'application/json; charset=utf-8'}
        params = {"access_token": self.token}
        if action == "PUT":
            dataJSON = {
                "psid": dest_id,
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
            params['psid'] = dest_id

            res = requests.delete(
                self.url + '/custom_user_settings',
                headers=header, params=params
            )
            Analyse(res)
            return res

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_file(self, dest_id, file, filetype="file", filename_=None):
        """
        this method send a local file

        Args:
            destId (str): user id facebook for the destination
            file (str): name of the file in local folder 
            filetype (str, optional): type of the file["video","image",...]. Defaults to "file".
            filename_ (str, optional): A filename received for de destination . Defaults to None.

        Returns:
            Response: POST request to the facebook API to send a file to the user
        """
        if filename_ is None:
            filename_ = file
        params = {
            "access_token": self.token
        }

        data = {
            'recipient': json.dumps({'id': dest_id}),

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
                open(f'data/{dest_id}/{file}', 'rb'),
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

    def send_template(self, dest_id,elements,payload):   
        res = elements
        if res:
            page = int(json.loads(req.get_temp(dest_id)).get("__page"))
            deb_indice = (page-1) * 10 if page else 1
            
            if len(res) > deb_indice + 10:
                self.send_result(
                    dest_id, res[deb_indice:deb_indice + 10],
                    next=[
                        {
                            "content_type": "text",
                            "title": "⏭️PAGE SUIVANTE",
                            "payload": payload,
                        }
                    ]
                )
                req.set_temp(dest_id,"__page",page+1)
            else:
                self.send_result(dest_id, res[deb_indice:deb_indice + 10])
        else:
            self.send_message(dest_id, "No Elements dispo")