from os import environ, makedirs, removedirs
from ampalibe import Messenger, Payload
from ampalibe.messenger import Action, Filetype
from ampalibe.ui import Button, Element, QuickReply, Type

chat = Messenger()
sender_id = environ.get("USER_ID")


def test_send_action():
    assert chat.send_action(sender_id, Action.mark_seen).status_code == 200


def test_send_text():
    assert chat.send_text(sender_id, "Hello world").status_code == 200


def test_send_quick_reply():
    makedirs("assets/private", exist_ok=True)
    quick_rep = [
        QuickReply(
            title="Angela",
            payload="/membre",
            image_url="https://i.imgflip.com/6b45bi.jpg",
        ),
        QuickReply(
            title="Rivo",
            payload="/membre",
            image_url="https://i.imgflip.com/6b45bi.jpg",
        ),
    ]
    assert (
        chat.send_quick_reply(sender_id, quick_rep, "who do you choose ?").status_code
        == 200
    )

    quick_rep = [
        QuickReply(
            title=f"response {i+1}",
            payload=Payload("/response", item=i + 1),
            image_url="https://i.imgflip.com/6b45bi.jpg",
        )
        for i in range(20)
    ]
    assert (
        chat.send_quick_reply(
            sender_id, quick_rep, "who do you choose ?", next="See More"
        ).status_code
        == 200
    )


def test_send_template():
    makedirs("assets/private", exist_ok=True)
    list_items = []

    for i in range(30):
        buttons = [
            Button(
                type=Type.postback,
                title="Get item",
                payload=Payload("/item", id_item=i + 1),
            )
        ]

        list_items.append(
            Element(
                title="iTem",
                image_url="https://i.imgflip.com/6b45bi.jpg",
                buttons=buttons,
            )
        )

    assert (
        chat.send_template(
            sender_id,
            list_items,
            next=True,
            quick_rep=[
                QuickReply(title="retour", payload="/return"),
            ],
        ).status_code
        == 200
    )

    assert (
        chat.send_template(sender_id, list_items, next="Next page").status_code == 200
    )


def test_send_file_url():
    assert (
        chat.send_file_url(
            sender_id, "https://i.imgflip.com/6b45bi.jpg", filetype=Filetype.image
        ).status_code
        == 200
    )


def test_send_button():
    buttons = [Button(title="Informations", payload="/contact")]

    assert (
        chat.send_button(sender_id, buttons, "What do you want to do?").status_code
        == 200
    )

def test_persitent_menu():
    persistent_menu = [
        Button(type='postback', title='Menu', payload='/payload'),
        Button(type='postback', title='Logout', payload='/logout')
    ]

    assert (
        chat.persistent_menu(sender_id, persistent_menu).status_code
        == 200
    )