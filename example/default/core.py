import ampalibe
from ampalibe import Payload
from conf import Configuration

query = ampalibe.Model()


@ampalibe.command("/")
def main(**extends):
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
    if query.get_temp(sender_id, "myname") == myname:
        return cmd + " " + myname
    return "Del temp error"
