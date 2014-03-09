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
from problem import problem
from web import form
import random
from collections import defaultdict
import compiler
import randomgenerator
import solver2
from solution import solutioninstance
from index import admin
from remove import remove
from modify import modify
from hinter import hinter
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
'/signout','reset'
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




def checksolution(idp,theircommands):
  data={}
  data['idp']=idp
  problemdata=db.select('description',data,where='id=$idp')
  problemdata=problemdata[0]
  commands=re.split('[\n\r]+',problemdata.recurrence)
  text='\n'.join(theircommands)
  for i in range(10):
    constants=randomgenerator.getRandomConstants(problemdata.constants)
    arrays=randomgenerator.getRandomArrays(problemdata.arrays)
    t=problem('<p>'+problemdata.description,arrays,constants,(problemdata.dimension_y,20),problemdata.solutiontext,problemdata.tableexplanation)
    mysolution=solutioninstance(solver2.solve(t.lists,t.constants,commands,t.dimensions[0],t.dimensions[1]))
    theirsolution=solutioninstance(solver2.solve(t.lists,t.constants,theircommands,t.dimensions[0],t.dimensions[1]))
    if mysolution.table==theirsolution.table:
      print "TRUE TRUE  TRUE!!!!!!!!!!!"
      
    else:
      print "FALSE FALSE FALSE!!!!"
      print mysolution.table
      print theirsolution.table
      db.insert('user_input',id_user=session.userid,attempt=text,id_problem=idp,correct=0)
      return False
  db.insert('user_input',id_user=session.userid,attempt=text,id_problem=idp,correct=1)
  try:
    db.insert('user_problems', id_user=session.userid,id_problem=idp)
  except:
    pass
  return True
      
  

class reset:
    def GET(self):
         session.kill()
         raise web.seeother('/signin')

dimensionform=form.Form(
    form.Textbox("dimensionx", description="Width"),
    form.Textbox("dimensiony", description="Height"),
    
    form.Button("submit", type="submit", description="Enter"),
    validators = [form.Validator("Wrong Dimension", lambda i: i.dimensionx == 'C' and i.dimensiony=='1')]
    )
    
	
class problemview:
  def GET(self):
    top()
    data=web.input()
    session.idp=data['idp']
    session.hintlevel=0
    session.hint=''
    form=dimensionform
    problemdata=db.select('description',data,where='id=$idp')
    problemdata=problemdata[0]
    constants=randomgenerator.getRandomConstants(problemdata.constants)
    arrays=randomgenerator.getRandomArrays(problemdata.arrays)
    
    t=problem('<p>'+problemdata.description,arrays,constants,(problemdata.dimension_y,20),problemdata.solutiontext,problemdata.tableexplanation)
    session.instance=t
    session.problemstatus=0
    return render.problemview(t,form)
  
 
  
  def POST(self):
    top()
    problemdata=db.select('description',session,where='id=$idp')
    problemdata=problemdata[0]
    commands=re.split('[\n\r]+',problemdata.recurrence)
    mysolution=solutioninstance(solver2.solve(session.instance.lists,session.instance.constants,commands,session.instance.dimensions[0],session.instance.dimensions[1]))
    comments=db.query('select * from example_users eu join comment c on c.user_id=eu.id where c.problem_id='+session.idp)
    mhinter=hinter()
    if session.hintlevel>0:
      session.hint=mhinter.hint(problemdata.recurrence,session.hintlevel)
    if session.problemstatus==1:
      f = dimensionform()
      data=web.input()
      if 'action' in data.keys():
	if data['action']=='table':
	    session.problemstatus=2
	    return render.problemtable(session.instance,mysolution,None,comments)
	if data['action']=='solution':
	  session.problemstatus=3
	  return render.solution(session.instance)
      if f.validates():
	session.problemstatus+=1
	return render.problemtable(session.instance,mysolution,None,comments)
      else:
	return render.problemview(session.instance,f)
    elif session.problemstatus==2:
      data=web.input()
      if 'recterms' in data:
        if 'hint' in data:
	  session.hintlevel=min(session.hintlevel+1,3)
	  session.hint=mhinter.hint(problemdata.recurrence,session.hintlevel)
	  return render.problemtable(session.instance,mysolution,None,comments,False)
	commands=re.split('[\n\r]+',data['recterms'])
	try:
	  correct=checksolution(session.idp,commands)
	  theirsolution=solutioninstance(solver2.solve(session.instance.lists,session.instance.constants,commands,session.instance.dimensions[0],session.instance.dimensions[1]))
	except:
	  correct=False
	  theirsolution=None
	  render.problemtable(session.instance,mysolution,None,comments,correct)
	return render.problemtable(session.instance,mysolution,theirsolution.table,comments,correct)
      if data['action']=='solution':
	  session.problemstatus=3
	  return render.solution(session.instance)
      elif data['action']=='new':
	problemdata=db.select('description',session,where='id=$idp')
	problemdata=problemdata[0]
	commands=re.split('[\n\r]+',problemdata.recurrence)
	constants=randomgenerator.getRandomConstants(problemdata.constants)
	session.instance.constants=constants
	arrays=randomgenerator.getRandomArrays(problemdata.arrays)
	session.instance.lists=arrays
	session.solutionindex=0	
	print constants
	mysolution=solutioninstance(solver2.solve(session.instance.lists,session.instance.constants,commands,session.instance.dimensions[0],session.instance.dimensions[1]))
    
	return render.problemtable(session.instance,mysolution,None,comments)
      elif data['action']=='showsolution':
	 mysolution.show=True
	 session.solutionindex=0
	 return render.problemtable(session.instance,mysolution,None,comments)
      elif data['action']=='nextvalue':
	 mysolution.show=True
	 session.solutionindex+=1
	 return render.problemtable(session.instance,mysolution,None,comments)
      elif data['action']=='comment':
	db.insert('comment', user_id=session.userid,problem_id=session.idp,comment=data['comment'])
	comments=db.query('select * from example_users eu join comment c on c.user_id=eu.id where c.problem_id='+session.idp)
    
	return render.problemtable(session.instance,mysolution,None,comments)
class collection:
  def GET(self):
    top()
    problems=db.select('problem')
    progress=db.select('user_problems',session,where='id_user=$userid')
    progress=[x.id_problem for x in progress]
    return render.collection(problems,progress)


   

class index:
    def GET(self):
      return str("hi")
if __name__ == "__main__":
    app.run()
    
application = app.wsgifunc()
