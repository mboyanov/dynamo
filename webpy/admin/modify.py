import web
import hashlib
from web import form
import config
from top import top
render = web.template.render(config.templatedir,base="layout")


def getForm(problem,description):
  problem_form = form.Form(
      form.Textbox("name", description="Problem Name:",class_='none',value=problem.name),
      form.Dropdown('difficulty', [('1', 'Easy'), ('2', 'Average'),('3', 'Hard'),('4', 'Very Hard')],description="Difficulty:",class_='none',value=problem['difficulty']),
      form.Number('dimension_x',form.notnull,description="Dimension X:",value=description['dimension_x'] ),
      form.Number('dimension_y',form.notnull,description="Dimension Y:",value=description['dimension_y']),
  )
  return problem_form
db = config.getDB()



class modify:
 
  def GET(self):
    top()
    problems=db.select('problem')
    return render.modifyall(problems)
  def POST(self):
    top()
    i=web.input()
    t=i.view[0]
    print t
    variables=dict(myid=t)
    description=db.select('description',vars=variables,where='id=$myid')
    problem=db.select('problem',vars=variables,where='id=$myid')
    problem=problem[0]
    description=description[0]
    f=getForm(problem,description)
    exec("description['constants']="+description['constants'])
    return render.modify(f,problem,description)
    