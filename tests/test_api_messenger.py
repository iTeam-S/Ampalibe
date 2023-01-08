from os import environ, makedirs, removedirs
from ampalibe import Messenger, Payload
from ampalibe.messenger import Action, Filetype
from ampalibe.ui import (
    Button,
    Element,
    QuickReply,
    Type,
    ReceiptElement,
    Summary,
    Adjustment,
    Address,
)

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


def test_send_generic_template():
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
        chat.send_generic_template(
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
        chat.send_generic_template(sender_id, list_items, next="Next page").status_code
        == 200
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
        Button(type="postback", title="Menu", payload="/payload"),
        Button(type="postback", title="Logout", payload="/logout"),
    ]

    assert chat.persistent_menu(sender_id, persistent_menu).status_code == 200


def test_send_receipt_template():
    receipts = [
        ReceiptElement(title="Tee-shirt", price=1000),
        ReceiptElement(title="Pants", price=2000),
    ]

    # create a summary
    summary = Summary(total_cost=300)

    # create an address
    address = Address(
        street_1="Street 1",
        city="City",
        state="State",
        postal_code="Postal Code",
        country="Country",
    )

    # create an adjustment
    adjustment = Adjustment(name="Discount of 10%", amount=10)

    assert (
        chat.send_receipt_template(
            sender_id,
            "Arleme",
            123461346131,
            "MVOLA",
            summary=summary,
            receipt_elements=receipts,
            currency="MGA",
            address=address,
            adjustments=[adjustment],
        ).status_code
    ) == 200


def test_personas_mangement():
    # create
    personas_id = chat.create_personas(
        "Rivo Lalaina", "https://avatars.githubusercontent.com/u/59861055?v=4"
    )
    assert personas_id.isdigit()

    # get personas
    personas = chat.get_personas(personas_id)
    assert personas.get("id") == personas_id

    # list personas
    list_personas = chat.list_personas()
    assert list_personas[0].get("id") == personas_id

    # delete personas
    assert chat.delete_personas(personas_id).status_code == 200


def test_send_onetime_notification_request():
    assert (
        chat.send_onetime_notification_request(
            sender_id, "Accepter le notification", "/test"
        ).status_code
        == 200
    )
