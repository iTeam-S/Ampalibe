import ampalibe
from conf import Configuration


@ampalibe.command('/')
def main(sender_id, cmd, **extends):    
    print("Hello, Ampalibe")
    
