import os
import sys
import time 
t = time.time()
# Mode Dev only 
sys.path.insert(0, os.path.dirname('/'.join(__file__.split('/')[:-1])))
if True:
    import ampalibe
    print(round(time.time() - t))
    from conf import Configuration
    print(round(time.time() - t))
    import core
    print(round(time.time() - t))
print(round(time.time() - t))
ampalibe.run(Configuration())
