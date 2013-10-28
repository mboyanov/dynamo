import web
import hashlib
from register import register
from signin import signin
from problem import problem
from web import form
import random
from collections import defaultdict
from Intknap import intknap
import compiler
import randomgenerator
import solver
from solution import solutioninstance


web.config.debug = False
urls = (
"/","index",
"/reset", "reset",	
'/register','register',
'/signin','signin',
'/problem','problemview',
'/collection','collection',
'/try','mytry',
)


app = web.application(urls, locals())
db = web.database(dbn='mysql', db='web', user='root', pw='')
store = web.session.DBStore(db, 'sessions')
session = web.session.Session(app, store, initializer={'count': 0,'login': 0, 'privilege': 0,'user' :'','idp':-1,'instance':['a'],'problemstatus':-1})
render = web.template.render('templates/',base='layout',globals={'context': session})


def session_hook():
    web.ctx.session = session

app.add_processor(web.loadhook(session_hook))


def logged():
    if session.login==1:
        return True
    else:
        return False


def create_render(privilege):
  render = web.template.render('templates/')
  return render



class reset:
    def GET(self):
         session.kill()
         return ""

dimensionform=form.Form(
    form.Textbox("dimensionx", description="Width"),
    form.Textbox("dimensiony", description="Height"),
    
    form.Button("submit", type="submit", description="Enter"),
    validators = [form.Validator("Wrong Dimension", lambda i: i.dimensionx == 'C' and i.dimensiony=='1')]
    )
    
	
class problemview:
  def GET(self):
    data=web.input()
    session.idp=data['idp']
    form=dimensionform
    problemdata=db.select('description',data,where='id=$idp')
    problemdata=problemdata[0]
    constants=randomgenerator.getRandomConstants(problemdata.constants)
    arrays=randomgenerator.getRandomArrays(problemdata.arrays)
    
    t=problem('<p>'+problemdata.description,arrays,constants,"fsa",(1,11),problemdata.solutiontext)
    session.instance=t
    session.problemstatus=1;
    return render.problemview(t,form)
  
 
  
  def POST(self):
    problemdata=db.select('description',session,where='id=$idp')
    problemdata=problemdata[0]
    commands=problemdata.recurrence.split('\n')
    
    mysolution=solutioninstance(solver.solve(session.instance.lists,session.instance.constants,commands,10,10))
    if session.problemstatus==1:
      f = dimensionform()
      data=web.input()
      if 'action' in data.keys():
	if data['action']=='table':
	    session.problemstatus=2
	    return render.problemtable(session.instance,mysolution)
	if data['action']=='solution':
	  session.problemstatus=3
	  return render.solution(session.instance)
      if f.validates():
	session.problemstatus+=1
	return render.problemtable(session.instance,mysolution)
      else:
	return render.problemview(session.instance,f)
    elif session.problemstatus==2:
      data=web.input()
      if 'recterms' in data:
	commands=data['recterms'].split('\n')
	theirsolution=solutioninstance(solver.solve(session.instance.lists,session.instance.constants,commands,10,10))
	return theirsolution.table
      if data['action']=='solution':
	  session.problemstatus=3
	  return render.solution(session.instance)
      elif data['action']=='new':
	problemdata=db.select('description',session,where='id=$idp')
	problemdata=problemdata[0]
	commands=problemdata.recurrence.split('\n')
	constants=randomgenerator.getRandomConstants(problemdata.constants)
	session.instance.constants=constants
	arrays=randomgenerator.getRandomArrays(problemdata.arrays)
	session.instance.lists=arrays
	
	
	print constants
	mysolution=solutioninstance(solver.solve(session.instance.lists,session.instance.constants,commands,10,10))
    
	return render.problemtable(session.instance,mysolution)
      elif data['action']=='showsolution':
	 mysolution.show=True
	 return render.problemtable(session.instance,mysolution)

class collection:
  def GET(self):
    problems=db.select('problem')
    return render.collection(problems)


   

class index:
    def GET(self):
      return str("hi")
if __name__ == "__main__":
    app.run()