import web
import hashlib
from web import form
from problem import problem
from solution import solutioninstance
import solver2
import randomgenerator
import config
import re

render = web.template.render(config.templatedir,base="layout")

problem_form = form.Form(
    form.Textbox("name",form.notnull, description="Problem Name:",class_='none'),
    form.Dropdown('difficulty', [('1', 'Easy'), ('2', 'Average'),('3', 'Hard'),('4', 'Very Hard')],description="Difficulty:",class_='none'),
    form.Number('dimension_x',form.notnull,form.Validator('Must be a positive value', lambda x:int(x)>0),description="Dimension X:", ),
    form.Number('dimension_y',form.notnull,form.Validator('Must be a positive value', lambda x:int(x)>0),description="Dimension Y:",),
)
def top():
  
  if web.ctx.session.user is None or web.ctx.session.user!='admin':
    raise web.seeother('/signin')
class admin:

  
  def GET(self):
    
    top()
    f=problem_form()
    return render.admin(f)
  def POST(self):
    top()
    i=web.input(constantsnames=[],constantsmin=[],constantsmax=[],arraysnames=[],arraysmin=[],arraysmax=[],arraysnum=[],hintsnames=[])
    f=problem_form()
    if f.validates()==False:
      return 'Please provide a name for the problem,a difficulty and positive dimensions'
    out=""
    db = web.database(dbn='mysql', db='web', user='root', pw='xaxaxa')
    hints=[]
    
    for  t in range(len(i.hintsnames)):
	if len(i.hintsnames[t])>0 and len(i.hintsnames[t])<400 :
	  try:
	    hints.append(i.hintsnames[t])
	  except:
	    try:
	      return 'problem with hint '+i.hintsnames[t]
	    except(NameError):
	      return 'problem with hint '+i.hintsnames[t]
	elif len(i.constantsnames[t])>400:
	  return 'Hint is too long - maximum 400 characters:'+i.hintsnames[t]
    constants=[]
    for  t in range(len(i.constantsnames)):
	if len(i.constantsnames[t])>0 and len(i.constantsnames[t])<100 :
	  try:
	    constants.append( (i.constantsnames[t],int(i.constantsmin[t]),int(i.constantsmax[t])))
	  except:
	    try:
	      return 'problem with constant '+i.constantsnames[t]+" max:"+i.constantsmax[t]+'.Are you sure the maximum and the minimum are integers?'
	    except(NameError):
	      return 'problem with constant '+i.constantsnames[t]
	elif len(i.constantsnames[t])>100:
	  return 'Name of constant is too big:'+i.constantsnames[t]
    arrays=[]
    for  t in range(len(i.arraysnames)):
	if len(i.arraysnames[t])>0 and len(i.arraysnames[t])<100 :
	  try:
	    if i.arraysnum[t]<=0:
	      return 'Number of items must be positive for array '+i.arraysnames[t]
	    if i.arraysmin[t]>i.arraysmax[t]:
	      return 'Max is less than min for array '+i.arraysnames[t]
	    arrays.append( (i.arraysnames[t],int(i.arraysnum[t]),int(i.arraysmin[t]),int(i.arraysmax[t])))
	  except BaseException as e:
	    
	    return 'problem with array '+i.arraysnames[t]+" max:"+i.arraysmax[t]+' Number of values:'+i.arraysnum[t]+'.Are you sure all the values are integers?'
	elif len(i.arraysnames[t])>100:
	  return 'Name of array is too big:'+i.arrayssnames[t]
    if i.description is None:
      return 'Please provide a description for the problem'
    if i.videourl is not None and len(i.videourl)>100:
      return "URL too long"
	
    constantsinst=randomgenerator.getRandomConstants(str(constants))
    arraysinst=randomgenerator.getRandomArrays(str(arrays))
    
    i.dimension_x=int(i.dimension_x)
    i.dimension_y=int(i.dimension_y)
    t=problem('<p>'+i.description,arraysinst,constantsinst,(i.dimension_y,i.dimension_x),'','')
    commands=re.split('[\n\r]+',i.recurrence)
    print t.constants
    mysolution=solutioninstance(solver2.solve(t.lists,t.constants,commands,t.dimensions[0],t.dimensions[1]))
    
    n = db.insert('problem', name=i.name,difficulty=i.difficulty)
    q=db.insert('description',id=n,description=i.description,recurrence=i.recurrence,dimension_x=i.dimension_x,dimension_y=i.dimension_y,solutiontext="",constants=str(constants),arrays=str(arrays),hints=str(hints),video=("\""+i.videourl+"\""))
    raise web.seeother('/problem?idp='+str(n))
   
    