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


web.config.debug = False
urls = (
"/","index",
"/count", "count",
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

class count:
    def GET(self):
	t=problem()
        session.count += 1
        return str(t.content)

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
    t=problem('<p>'+problemdata.description,[('weights',[1,2,3]),('values',[1,1,3])],[('C',10)],"fsa",(1,11),problemdata.solutiontext)
    session.instance=t
    session.problemstatus=1;
    return render.problemview(t,form)
  
 
  
  def POST(self):
    solution=intknap(session.instance.lists['weights'],session.instance.lists['values'],session.instance.constants['C'])
    if session.problemstatus==1:
      f = dimensionform()
      data=web.input()
      if 'action' in data.keys():
	if data['action']=='table':
	    session.problemstatus=2
	    return render.problemtable(session.instance,solution)
	if data['action']=='solution':
	  session.problemstatus=3
	  return render.solution(session.instance)
      if f.validates():
	session.problemstatus+=1
	return render.problemtable(session.instance,solution)
      else:
	return render.problemview(session.instance,f)
    elif session.problemstatus==2:
      data=web.input()
      if data['action']=='ff':
	return 'xaxa'
      if data['action']=='solution':
	  session.problemstatus=3
	  return render.solution(session.instance)
      elif data['action']=='new':
	lists=session.instance.lists
	newlists={}
	
	for l in lists:
	  for i in range(len(lists[l])):
	    if l in newlists:
	      newlists[l].append(random.randint(1,10))
	    else:
	        newlists[l]=[random.randint(1,10)]
	    
	session.instance.lists=newlists
	solution=intknap(session.instance.lists['weights'],session.instance.lists['values'],session.instance.constants['C'])
	return render.problemtable(session.instance,solution)
      elif data['action']=='showsolution':
	 solution.show=True
	 return render.problemtable(session.instance,solution)

class collection:
  def GET(self):
    problems=db.select('problem')
    return render.collection(problems)


class mytry:
  def GET(self):
    f=open('myparser.py','r')
    source=f.read()
    f.close()
    compiler.compileFile('myparser.py')
    import myparser
    reload(myparser)
    a=myparser.getVar('T(1)')
    
    
    return a
    

class index:
    def GET(self):
      return str("hi")
if __name__ == "__main__":
    app.run()