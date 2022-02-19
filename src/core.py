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
bot = ampalibe.Messenger(Configuration.ACCESS_TOKEN)


@ampalibe.commande('/')
def main(sender_id, cmd, **extends):
    bot.send_message(sender_id, "Hello, world")
    bot.send_message(sender_id, "Entrer votre nom")
    req.set_action(sender_id, "/getname")

@ampalibe.action("/getname")
def getname(sender_id, cmd, **extends):
    req.set_temp(sender_id, 'nom', cmd)
    bot.send_message(sender_id, "OK, enrrgistrer")
    req.set_action(sender_id, None)

@ampalibe.commande('/myname')
def myname(sender_id, cmd, **extends):
    nom = req.get_temp(sender_id, 'nom')
    if nom:
        bot.send_message(sender_id, f"Bonjour {nom}")
    else:
        bot.send_message(sender_id, "Bonjour unknown")

@ampalibe.commande('/delmyname')
def delmyname(sender_id, cmd, **extends):
    req.del_temp(sender_id, 'nom')
    bot.send_message(sender_id, "ok")
