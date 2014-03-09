import os
import sys
templatedir = os.path.abspath(os.path.join(os.path.dirname(__file__), './templates'))
del os
del sys
import web

def getDB():
    return web.database(dbn='mysql', db='web', user='root', pw='xaxaxa')