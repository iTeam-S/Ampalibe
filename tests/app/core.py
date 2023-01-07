import ampalibe
from ampalibe import Payload
from conf import Configuration

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
