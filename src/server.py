import os
import sys
if True:
    '''
        mode dev, mbola misy an ty, fa ref atao pip install ampilabe
        de tsy mila an ito tsony, fa mbola precisena eto le dossier
        misy an le ampalibe afana mi import aza. atao anaty path
    '''
    sys.path.insert(0, os.path.dirname('/'.join(__file__.split('/')[:-1])))
    import ampalibe
    from controllers import core

ampalibe.run()


