import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), './admin'))
if not path in sys.path:
    sys.path.insert(1, path)
path = os.path.abspath(os.path.join(os.path.dirname(__file__), './'))
if not path in sys.path:
    sys.path.insert(1, path)
import web
import hashlib
from register import register
from signin import signin
from web import form
import random
from collections import defaultdict
import compiler
from index import admin
from remove import remove
from modify import modify
from hinter import hinter
from achievements import achievements
from problemview import problemview
import re

web.config.debug = False
urls = (
"/","index",
"/reset", "reset",	
'/register','register',
'/signin','signin',
'/problem','problemview',
'/collection','collection',
'/try','mytry',
'/admin','admin',
'/remove','remove',
'/modify','modify',
'/signout','reset',
'/achievements','achievements'
)


app = web.application(urls, globals())
db = web.database(dbn='mysql', db='web', user='root', pw='xaxaxa')
store = web.session.DBStore(db, 'sessions')

session = web.session.Session(app, store, initializer={'solutionindex': 0,'login': 0, 'privilege': 0,'user' :'','userid':'','idp':-1,'instance':['a'],'problemstatus':-1,'hintlevel':0,'hint':''})

import config


render = web.template.render(config.templatedir,base='layout',globals={'context': session})

def top():
  if web.ctx.session.user is None or web.ctx.session.user=='':
    raise web.seeother('/signin')

def session_hook():
    web.ctx.session = session

app.add_processor(web.loadhook(session_hook))


def logged():
    if session.login==1:
        return True
    else:
        return False





  

class reset:
    def GET(self):
         session.kill()
         raise web.seeother('/signin')

class collection:
  def GET(self):
    top()
    problems=db.select('problem')
    progress=db.select('user_problems',session,where='id_user=$userid')
    progress=[x.id_problem for x in progress]
    return render.collection(problems,progress)


   

class index:
    def GET(self):
      raise web.seeother('/signin')
if __name__ == "__main__":
    app.run()
    
application = app.wsgifunc()