import os
import sys
# Mode Dev only 
sys.path.insert(0, os.path.dirname('/'.join(__file__.split('/')[:-1])))
if True:
    import ampalibe
    import controllers.core
    from conf import Configuration

ampalibe.run(Configuration())
