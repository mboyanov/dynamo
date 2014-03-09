import web
import hashlib
from web import form
import config

render = web.template.render(config.templatedir,base="layout")

problem_form = form.Form(
    form.Textbox("name", description="Problem Name:",class_='none'),
    form.Dropdown('difficulty', [('1', 'Easy'), ('2', 'Average'),('3', 'Hard'),('4', 'Very Hard')],description="Difficulty:",class_='none'),
    form.Number('dimension_x',form.notnull,description="Dimension X:", ),
    form.Number('dimension_y',form.notnull,description="Dimension Y:",),
)
db = web.database(dbn='mysql', db='web', user='root', pw='xaxaxa')

def top():
  
  if web.ctx.session.user is None or web.ctx.session.user!='admin':
    raise web.seeother('/signin')

class remove:
 
    
  def GET(self):
    top()
    problems=db.select('problem')
    return render.remove(problems)
  def POST(self):
    top()
    i=web.input(remove=[])
    for t in i.remove:
      print t
      variables=dict(myid=t)
      a=db.delete('description',vars=variables,where='id=$myid')
      
      db.delete('problem',vars=variables,where='id=$myid')
    raise web.seeother('/collection')
   
    