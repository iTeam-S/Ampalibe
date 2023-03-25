import ampalibe
from conf import Configuration
from ampalibe import Payload
from ampalibe.utils import translate
from ampalibe.utils import async_simulate as simulate
from ampalibe.utils import async_download_file as download_file

query = ampalibe.Model()


@ampalibe.command("/")
def main(sender_id, **extends):
    print(query.get_temp(sender_id, "token"))
    return "Hello Ampalibe"


@ampalibe.command("/set_my_name")
def set_my_name(**extends):
    res = Payload("/get_my_name", myname="Ampalibe")
    return Payload.trt_payload_out(res)


@ampalibe.command("/get_my_name")
def get_my_name(myname, **extends):
    """
    Verify if payload parameter work here
    """
    return myname


@ampalibe.command("/try_action")
def try_action(sender_id, **extends):
    query.set_action(sender_id, "/action_work")
    query.set_temp(sender_id, "myname", "Ampalibe")


@ampalibe.action("/action_work")
def action_work(sender_id, cmd, **extends):
    query.set_action(sender_id, None)
    myname = query.get_temp(sender_id, "myname")
    query.del_temp(sender_id, "myname")
    if query.get_temp(sender_id, "myname") != myname:
        return cmd + " " + myname
    return "Del temp error"


@ampalibe.command("/try_second_action")
def try_second_action(sender_id, **extends):
    query.set_action(
        sender_id, Payload("/second_action_work", myname="Ampalibe", version=2)
    )


@ampalibe.action("/second_action_work")
def second_action_work(sender_id, cmd, myname, version, **extends):
    query.set_action(sender_id, None)
    return cmd + " " + myname + str(version)


@ampalibe.command("/receive_optin_webhook")
def receive_optin_webhook(**extends):
    return "Optin"


@ampalibe.command("/lang")
async def lang(sender_id, value=None, **extends):
    if value:
        query.set_lang(sender_id, value)
        await simulate(sender_id, "/lang/download")
    return Payload.trt_payload_out(Payload("/lang", value="en"))


@ampalibe.command("/lang/download")
async def lang_download(lang, **extends):
    await download_file(
        f"http://127.0.0.1:{Configuration.APP_PORT}/asset/hello.txt",
        "assets/private/hello.txt",
    )


@ampalibe.command("/lang/test")
def lang_test(lang, **extends):
    with open("assets/private/hello.txt", "r") as f:
        text = f.read().strip()
    return translate(text, lang)
