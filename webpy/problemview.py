import web
import config
import randomgenerator
import re
from hinter import hinter
from solution import solutioninstance
from problem import problem
import solver2
from ParserException import ParserException
from achievementchecker import achievementchecker
from top import top
from solutionchecker import checksolution
from buttonhitter import buttonhitter
db = config.getDB()
render=None


      
  


class problemview:
  def GET(self):
    top()

    data=web.input()
    web.ctx.session.idp=data['idp']
    web.ctx.session.hintlevel=0
    web.ctx.session.hint=''
    problemdata=db.select('description',data,where='id=$idp')
    problemdata=problemdata[0]
    constants=randomgenerator.getRandomConstants(problemdata.constants)
    arrays=randomgenerator.getRandomArrays(problemdata.arrays)
    if problemdata.hints is not None:
      hinttext='hints='+problemdata.hints
      exec(hinttext)
    else:
      hints=None
    if problemdata.video is not None:
      videotext='video='+problemdata.video
      exec(videotext)
    else :
      video=None    
    t=problem('<p>'+problemdata.description,arrays,constants,(problemdata.dimension_y,20),problemdata.solutiontext,problemdata.tableexplanation,hints,video)
    web.ctx.session.instance=t
    web.ctx.session.problemstatus=2;
    web.ctx.session.solutionindex=0;
    commands=re.split('[\n\r]+',problemdata.recurrence)
    comments=db.query('select * from example_users eu join comment c on c.user_id=eu.id where c.problem_id='+web.ctx.session.idp)
    mysolution=solutioninstance(solver2.solve(web.ctx.session.instance.lists,web.ctx.session.instance.constants,commands,web.ctx.session.instance.dimensions[0],web.ctx.session.instance.dimensions[1]))
    render = web.template.render(config.templatedir,base='layout',globals={'context': web.ctx.session})
    return render.problemtable(web.ctx.session.instance,mysolution,None,comments)
  

  def POST(self):
    top()
    mbuttonhitter=buttonhitter()

    render = web.template.render(config.templatedir,base='layout',globals={'context': web.ctx.session})
    problemdata=db.select('description',web.ctx.session,where='id=$idp')
    problemdata=problemdata[0]
    commands=re.split('[\n\r]+',problemdata.recurrence)
    comments=db.query('select * from example_users eu join comment c on c.user_id=eu.id where c.problem_id='+web.ctx.session.idp)
    mhinter=hinter()
    mysolution=solutioninstance(solver2.solve(web.ctx.session.instance.lists,web.ctx.session.instance.constants,commands,web.ctx.session.instance.dimensions[0],web.ctx.session.instance.dimensions[1]))  
    if web.ctx.session.hintlevel>0:
      web.ctx.session.hint=mhinter.hint(problemdata.recurrence,web.ctx.session.hintlevel)
    data=web.input()
    scroll=None
    if 'scroll' in data:
        scroll=data['scroll']
    if 'recterms' in data:
      if 'hint' in data:
        web.ctx.session.hintlevel=min(web.ctx.session.hintlevel+1,3)
        web.ctx.session.hint=mhinter.hint(problemdata.recurrence,web.ctx.session.hintlevel)
        mbuttonhitter.hitHints()
        return render.problemtable(web.ctx.session.instance,mysolution,None,comments,False,scroll=scroll)
      else:
          mbuttonhitter.hitCommands()
      commands=re.split('[\n\r]+',data['recterms'])
      message=''
      theirsolution=None
      try:
        theirsolution=solutioninstance(solver2.solve(web.ctx.session.instance.lists,web.ctx.session.instance.constants,commands,web.ctx.session.instance.dimensions[0],web.ctx.session.instance.dimensions[1]))
        print "THEIR SOLUTION:",theirsolution.table
        correct,checks=checksolution(web.ctx.session.idp,commands)	
        
        if correct:
          achecker=achievementchecker()
          message=achecker.check(web.ctx.session.userid)
          mbuttonhitter.hitCorrectCommands()

      except ParserException as e:
        correct=False
        if theirsolution is not None:
          return render.problemtable(web.ctx.session.instance,mysolution,theirsolution.table,comments,correct,e.message,theircommands=data['recterms'],scroll=scroll)
        else:
          return render.problemtable(web.ctx.session.instance,mysolution,None,comments,correct,e.message,theircommands=data['recterms'],scroll=scroll)
      except (NameError,SyntaxError) as e:
        correct=False
        if theirsolution is not None:
          return render.problemtable(web.ctx.session.instance,mysolution,theirsolution.table,comments,correct,str(e),theircommands=data['recterms'],scroll=scroll)
        else:
          return render.problemtable(web.ctx.session.instance,mysolution,None,comments,correct,str(e),theircommands=data['recterms'],scroll=scroll)
      except:
          correct=False
          if theirsolution is not None:
            return render.problemtable(web.ctx.session.instance,mysolution,theirsolution.table,comments,correct,"Something went wrong",theircommands=data['recterms'],scroll=scroll)
          else:
	    return render.problemtable(web.ctx.session.instance,mysolution,None,comments,correct,"Something went wrong",theircommands=data['recterms'],scroll=scroll)
      print "received checks length" ,len(checks)
      return render.problemtable(web.ctx.session.instance,mysolution,theirsolution.table,comments,correct=correct,message=message,theircommands=data['recterms'],checks=checks,scroll=scroll)
    
    if data['action']=='new':
      constants=randomgenerator.getRandomConstants(problemdata.constants)
      web.ctx.session.instance.constants=constants
      arrays=randomgenerator.getRandomArrays(problemdata.arrays)
      web.ctx.session.instance.lists=arrays
      web.ctx.session.solutionindex=0	

      mysolution=solutioninstance(solver2.solve(web.ctx.session.instance.lists,web.ctx.session.instance.constants,commands,web.ctx.session.instance.dimensions[0],web.ctx.session.instance.dimensions[1]))
  
      return render.problemtable(web.ctx.session.instance,mysolution,None,comments,scroll=scroll)
    elif data['action']=='showsolution':
	mysolution.show=True
	web.ctx.session.solutionindex=mysolution.length
	return render.problemtable(web.ctx.session.instance,mysolution,None,comments,scroll=scroll)
    elif data['action']=='nextvalue':
	mysolution.show=True
	web.ctx.session.solutionindex+=1
	return render.problemtable(web.ctx.session.instance,mysolution,None,comments,scroll=scroll)
    elif data['action']=='comment':
      db.insert('comment', user_id=web.ctx.session.userid,problem_id=web.ctx.session.idp,comment=data['comment'])
      comments=db.query('select * from example_users eu join comment c on c.user_id=eu.id where c.problem_id='+web.ctx.session.idp)
  
      return render.problemtable(web.ctx.session.instance,mysolution,None,comments,scroll=scroll)
