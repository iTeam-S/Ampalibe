import os
import json
import pickle
import requests
from sys import stderr
from retry import retry
import requests_toolbelt
from .utils import Payload
from conf import Configuration  # type: ignore
from .ui import QuickReply, Button, Element


class Messenger:
    def __init__(self, log_level="error"):
        """
        Here, We need the <access token> of the facebook page we want
        to apply the bot for the purpose of page and bot interaction

        Args:
            access_token (str): A facebook page access token
            log_level (error, info, quiet): A type of display log
                error: print only error
                info: print access log and error log
                quiet: do not print anything
        """
        self.access_token = Configuration.ACCESS_TOKEN
        self.url = "https://graph.facebook.com/v13.0/me"

        if log_level not in ("error", "info", "quiet"):
            raise Exception(ValueError, "log_level must be error or info or quiet")

    def __analyse(self, res, log_level="error"):
        if log_level == "info":
            print(res.status_code, res.text)
        elif res.status_code != 200 and log_level == "error":
            print(res.status_code, res.text, file=stderr)
        return res

    @property
    def token(self):
        if self.access_token.strip() == "":
            print("Warning! EMPTY PAGE ACCESS TOKEN", file=stderr)
        return self.access_token

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_custom(self, json, endpoint="/messages"):
        """
        This method send a custom json,
        use for the api not implemented in ampalibe.

        Args:
            json: A json object
            endpoint: A endpoint of facebook api
                /messages by default like other endpoint
        """
        header = {"content-type": "application/json; charset=utf-8"}
        params = {"access_token": self.token}

        res = requests.post(
            self.url + endpoint, json=json, headers=header, params=params
        )
        return self.__analyse(res)

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_message(self, dest_id, message, prio=False):
        """
        This method allows you to send a text message to the given recipient,
        Note that the number of characters to send is limited to 2000 characters

        Args:
            dest_id (str): user id facebook for the destination
            message (str): message want to send

        Returns:
            Response: POST request to the facebook API to send a message to the user

        Ref:
            https://developers.facebook.com/docs/messenger-platform/send-messages#sending_text
        """
        self.send_action(dest_id, "typing_on")
        data_json = {"recipient": {"id": dest_id}, "message": {"text": message}}

        if prio:
            data_json["messaging_type"] = "MESSAGE_TAG"
            data_json["tag"] = "ACCOUNT_UPDATE"

        header = {"content-type": "application/json; charset=utf-8"}
        params = {"access_token": self.token}

        res = requests.post(
            self.url + "/messages", json=data_json, headers=header, params=params
        )
        self.send_action(dest_id, "typing_off")
        return self.__analyse(res)

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

        Ref:
            https://developers.facebook.com/docs/messenger-platform/send-messages/sender-actions
        """
        data_json = {
            "messaging_type": "RESPONSE",
            "recipient": {"id": dest_id},
            "sender_action": action,
        }

        header = {"content-type": "application/json; charset=utf-8"}
        params = {"access_token": self.token}

        res = requests.post(
            self.url + "/messages", json=data_json, headers=header, params=params
        )
        return self.__analyse(res)

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_quick_reply(self, dest_id, quick_reps, text, next=False):
        """
        Quick replies provide a way to present a set of up to 13 buttons
        in-conversation that contain a title and optional image, and appear
        prominently above the composer. You can also use quick replies
        to request a person's location, email address, and phone number.

        Args:
            dest_id (str): user id facebook for the destination
            quick_rep (list of dict) || (list of QuickRep): list of the different quick_reply to send a user
            text (str): A text of a little description for each <quick_reply>
            next(bool) || (text): this params activate the next page when elements have a length more than ten

        Returns:
            Response: POST request to the facebook API to send a quick_reply to the user

        Ref:
            https://developers.facebook.com/docs/messenger-platform/send-messages/quick-replies
        """

        quick_reps = [
            quick_rep.value if isinstance(quick_rep, QuickReply) else quick_rep
            for quick_rep in quick_reps
        ]

        dataJSON = {
            "messaging_type": "RESPONSE",
            "recipient": {"id": dest_id},
            "message": {"text": text, "quick_replies": quick_reps[:13]},
        }

        if len(quick_reps) > 13 and next:
            dataJSON["message"]["quick_replies"][12] = {
                "content_type": "text",
                "title": "More" if next == True else str(next),
                "payload": "/__more",
                "image_url": "https://icon-icons.com/downloadimage.php"
                + "?id=81300&root=1149/PNG/512/&file="
                + "1486504364-chapter-controls-forward-play"
                + "-music-player-video-player-next_81300.png",
            }

            pickle.dump(
                (quick_reps[13:], text, next), open(f"assets/private/.__{dest_id}", "wb")
            )

        header = {"content-type": "application/json; charset=utf-8"}
        params = {"access_token": self.token}

        res = requests.post(
            self.url + "/messages", json=dataJSON, headers=header, params=params
        )
        return self.__analyse(res)

    def send_result(self, **ext):
        raise Exception("Deprecated: Use send_template instead!")

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_template(self, dest_id, elements, quick_rep=None, next=None):
        """
        The method represent a Message templates who offer a way for you
        to offer a richer in-conversation experience than standard text messages by integrating
        buttons, images, lists, and more alongside text a single message. Templates can be use for
        many purposes, such as displaying product information, asking the messagerecipient to choose
        from a pre-determined set of options, and showing search results.

        For this, messenger only validates 10 templates
        for the first display, so we put the parameter
        <next> to manage these numbers if it is a number of
        elements more than 10,

        So, there is a quick_reply which acts as a "next page"
        displaying all requested templates

        Args:
            dest_id (str): user id facebook for the destination
            elements (list of dict) || (list of Element): the list of the specific elements to define the
            structure for the template
            quick_rep (list of dict) || (list of QuickReply): addition quick reply at the bottom of the template
            next(bool) || (text): this params activate the next page when elements have a length more than ten

        Returns:
            Response: POST request to the facebook API to send a template generic to the user

        Ref:
            https://developers.facebook.com/docs/messenger-platform/send-messages/template/generic
        """

        elements = [
            element.value if isinstance(element, Element) else element
            for element in elements
        ]

        dataJSON = {
            "messaging_type": "RESPONSE",
            "recipient": {"id": dest_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements[:10],
                    },
                },
            },
        }

        if len(elements) > 10 and next:
            dataJSON["message"]["quick_replies"] = [
                {
                    "content_type": "text",
                    "title": "Next" if next == True else str(next),
                    "payload": "/__next",
                    "image_url": "https://icon-icons.com/downloadimage.php"
                    + "?id=81300&root=1149/PNG/512/&file="
                    + "1486504364-chapter-controls-forward-play"
                    + "-music-player-video-player-next_81300.png",
                }
            ]
            pickle.dump(
                (elements[10:], next), open(f"assets/private/.__{dest_id}", "wb")
            )

        if quick_rep:
            for i in range(len(quick_rep)):
                if isinstance(quick_rep[i], QuickReply):
                    quick_rep[i] = quick_rep[i].value
                    if quick_rep[i].get("payload"):
                        quick_rep[i]["payload"] = Payload.trt_payload_out(
                            quick_rep[i]["payload"]
                        )
            dataJSON["message"]["quick_replies"] = quick_rep

        header = {"content-type": "application/json; charset=utf-8"}
        params = {"access_token": self.token}

        res = requests.post(
            self.url + "/messages", json=dataJSON, headers=header, params=params
        )
        return self.__analyse(res)

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_file_url(self, dest_id, url, filetype="file"):
        """
        The Messenger Platform allows you to attach assets to messages, including audio,
        video, images, and files.All this is the role of this Method. The maximum attachment
        size is 25 MB. The maximum resolution for images is 85 Megapixel. There are three ways
        to attach an asset to a message:

        Args:
            dest_id (str): user id facebook for destination
            url (str): the origin url for the file
            filetype (str, optional): type of the file["video","image",...]. Defaults to 'file'.

        Returns:
            Response: POST request to the facebook API to send a template generic to the user

        Ref:
            https://developers.facebook.com/docs/messenger-platform/send-messages#url
        """

        dataJSON = {
            "messaging_type": "RESPONSE",
            "recipient": {"id": dest_id},
            "message": {
                "attachment": {
                    "type": filetype,
                    "payload": {"url": url, "is_reusable": True},
                }
            },
        }
        header = {"content-type": "application/json; charset=utf-8"}
        params = {"access_token": self.token}
        res = requests.post(
            self.url + "/messages", json=dataJSON, headers=header, params=params
        )
        return self.__analyse(res)

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def persistent_menu(self, dest_id, menu, action="PUT", **kwargs):
        """
        The Persistent Menu disabling the composer best practices allows you to have an always-on
        user interface element inside Messenger conversations. This is an easy way to help people
        discover and access the core functionality of your Messenger bot at any point in the conversation

        Args:
            dest_id (str): user id for destination
            persistent_menu (list of dict) || (list of Button): the elements of the persistent menu to enable
            action (str, optional): the action for benefit["PUT","DELETE"]. Defaults to 'PUT'.

            locale [optionnel]
            composer_input_disabled [optionnel]

        Ref:
            https://developers.facebook.com/docs/messenger-platform/send-messages/persistent-menu
        """
        header = {"content-type": "application/json; charset=utf-8"}
        params = {"access_token": self.token}

        menu = [
            button.value if isinstance(button, Button) else button
            for button in menu
        ]

        if action == "PUT":
            dataJSON = {
                "psid": dest_id,
                "persistent_menu": [
                    {
                        "locale": kwargs.get("locale", "default"),
                        "composer_input_disabled": kwargs.get(
                            "composer_input_disabled", "false"
                        ),
                        "call_to_actions": menu,
                    }
                ],
            }

            res = requests.post(
                self.url + "/custom_user_settings",
                json=dataJSON,
                headers=header,
                params=params,
            )
            return self.__analyse(res)

        elif action == "DELETE":
            params["params"] = "(persistent_menu)"
            params["psid"] = dest_id

            res = requests.delete(
                self.url + "/custom_user_settings", headers=header, params=params
            )
            return self.__analyse(res)

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_file(self, dest_id, file, filetype="file", filename=None):
        """
        this method send an attachment from file

        Args:
            destId (str): user id facebook for the destination
            file (str): name of the file in local folder
            filetype (str, optional): type of the file["video","image",...]. Defaults to "file".
            filename (str, optional): A filename received for de destination . Defaults to None.

        Returns:
            Response: POST request to the facebook API to send a file to the user

        Ref:
            https://developers.facebook.com/docs/messenger-platform/send-messages#file
        """
        if filename is None:
            filename = file
        params = {"access_token": self.token}

        data = {
            "recipient": json.dumps({"id": dest_id}),
            "message": json.dumps(
                {
                    "attachment": {
                        "type": filetype,
                        "payload": {
                            "is_reusable": True,
                        },
                    }
                }
            ),
            "filedata": (
                os.path.basename(filename),
                open(file, "rb"),
                f"{filetype}/{file.split('.')[-1]}",
            ),
        }

        # multipart encode the entire payload
        multipart_data = requests_toolbelt.MultipartEncoder(data)

        # multipart header from multipart_data
        header = {"Content-Type": multipart_data.content_type}

        res = requests.post(
            self.url + "/messages", params=params, headers=header, data=multipart_data
        )
        return self.__analyse(res)

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_media(self, dest_id, fb_url, media_type):
        """
        Method that sends files media as image and video via facebook link.
        This model does not allow any external URLs, only those on Facebook.

        Args:
            destId (str): user id facebook for the destination
            fb_url (str): url of the media to send on facebook
                for this: To get the Facebook URL of an image or video, follow these steps:
                    -Click on the image or video thumbnail to open the full-size view
                    -Copy the URL address from your browser's address bar.
            media_type (str): the type of the media who to want send, available["image","video"]

        Returns:
            Response: POST request to the facebook API to send a media file using url facebook

        Ref:
            https://developers.facebook.com/docs/messenger-platform/send-messages/template/media
        """
        dataJSON = {
            "recipient": {"id": dest_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "media",
                        "elements": [{"media_type": media_type, "url": fb_url}],
                    },
                }
            },
        }

        header = {"content-type": "application/json; charset=utf-8"}
        params = {"access_token": self.token}

        res = requests.post(
            "https://graph.facebook.com/v6.0/me/messages",
            json=dataJSON,
            headers=header,
            params=params,
        )
        return self.__analyse(res)

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def get_started(self, payload="/"):
        """
        Method that GET STARTED button
        when the user talk first to the bot.

        Returns:
            Response: POST request to the facebook API to send a media file using url facebook

        Ref:
            https://developers.facebook.com/docs/messenger-platform/reference/messenger-profile-api/get-started-button
        """

        dataJSON = {"get_started": {"payload": payload}}

        header = {"content-type": "application/json; charset=utf-8"}
        params = {"access_token": self.token}

        res = requests.post(
            "https://graph.facebook.com/v6.0/me/messenger_profile",
            json=dataJSON,
            headers=header,
            params=params,
        )
        return self.__analyse(res)

    @retry(requests.exceptions.ConnectionError, tries=3, delay=3)
    def send_button(self, dest_id, buttons, text):
        """
        The button template sends a text message with
        up to three buttons attached. This template gives
        the message recipient different options to choose from,
        such as predefined answers to questions or actions to take.

         Args:
             dest_id (str): user id facebook for the destination
             buttons (list of dict) || (list of Button): The list of buttons who want send
             text (str): A text to describe the fonctionnality of the buttons

         Returns:
             Response: POST request to the facebook API to send all different buttons

         Ref:
             https://developers.facebook.com/docs/messenger-platform/send-messages/template/button
        """

        for i in range(len(buttons)):
            if isinstance(buttons[i], Button):
                buttons[i] = buttons[i].value
            if buttons[i].get("payload"):
                buttons[i]["payload"] = Payload.trt_payload_out(buttons[i]["payload"])

        self.send_action(dest_id, "typing_on")
        data_json = {
            "recipient": {"id": dest_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": buttons,
                    },
                }
            },
        }

        header = {"content-type": "application/json; charset=utf-8"}
        params = {"access_token": self.token}

        self.send_action(dest_id, "typing_off")
        res = requests.post(
            self.url + "/messages", json=data_json, headers=header, params=params
        )
        return self.__analyse(res)
