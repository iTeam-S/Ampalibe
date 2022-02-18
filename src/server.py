import os
import sys
from dotenv import load_dotenv
sys.path.insert(0, os.path.dirname('/'.join(__file__.split('/')[:-1])))
load_dotenv()
if True:
    import ampalibe
    from controllers import core

ampalibe.run()
