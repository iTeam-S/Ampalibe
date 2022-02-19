import ampalibe
from conf import Configuration

'''
    Principal fonction, où les messages réçu sur
    la page facebook rentrent.

    @param user_id: identifiant facebook de l'exp.
    @param cmd: message de la personne.
    @param extends: contiennent la liste des autres
        données envoyé par facebook (heure d'envoi, ...)
'''
req = ampalibe.req(Configuration())


@ampalibe.commande('/')
def main(sender_id, cmd, **extends):
    print("Hello, world")
    req.del_temp(sender_id, "nom")


@ampalibe.commande('/test')
def test(sender_id, cmd, **extends):
    req.set_action(sender_id, "/getname")
    req.set_temp(sender_id, 'nom', 'Gaetan')


@ampalibe.action('/getname')
def getname(sender_id, cmd, **extends):
    print("Bonjour", cmd)
    print(req.get_temp(sender_id, 'nom'))
    req.set_action(sender_id, None)
