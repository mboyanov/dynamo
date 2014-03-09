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
db = config.getDB()
render=None


def checksolution(idp, theircommands):
    checks = []
    data = {}
    answer = True
    data['idp'] = idp
    problemdata = db.select('description', data, where='id=$idp')
    problemdata = problemdata[0]
    commands = re.split('[\n\r]+', problemdata.recurrence)
    text = '\n'.join(theircommands)
    for i in range(10):
        constants = randomgenerator.getRandomConstants(problemdata.constants)
        arrays = randomgenerator.getRandomArrays(problemdata.arrays)
        t = problem('<p>' + problemdata.description, arrays, constants, (problemdata.dimension_y, 20),
                    problemdata.solutiontext, problemdata.tableexplanation)
        mysolution = solutioninstance(solver2.solve(t.lists, t.constants, commands, t.dimensions[0], t.dimensions[1]))
        theirsolution = solutioninstance(
            solver2.solve(t.lists, t.constants, theircommands, t.dimensions[0], t.dimensions[1]))
        #both answers are none-just output tables
        if mysolution.answer is None and theirsolution.answer is None:

            if mysolution.table == theirsolution.table:
                print "Try " + str(i) + ":", "TRUE TRUE  TRUE!!!!!!!!!!!"

                checks.append(["Succeeded with input:", constants, arrays, mysolution.table, theirsolution.table])
            else:
                checks.append(["Failed with input:", constants, arrays, mysolution.table, theirsolution.table])
                print "FALSE FALSE FALSE!!!!"
                print "mine:" + str(mysolution.table)
                print "theirs:" + str(theirsolution.table)
                answer = False
        #if one answer is None, return false. TODO: make them separate when you get messages
        elif (mysolution.answer is not None and theirsolution.answer is None) or (
                        mysolution.answer is None and theirsolution.answer is not None):
            checks.append(["You should specify an answer with the answer keyword",constants,arrays,mysolution.table,theirsolution.table,mysolution.answer,theirsolution.answer])
            answer = False
        elif mysolution.answer != theirsolution.answer:
            checks.append(["Wrong answer for input:", constants, arrays, mysolution.table,theirsolution.table, mysolution.answer,
                           theirsolution.answer])
            answer = False
        elif mysolution.answer == theirsolution.answer:
            checks.append(
                ["Succeeded with input:", constants, arrays, mysolution.table, theirsolution.table, mysolution.answer,
                 theirsolution.answer])
    try:
        db.insert('user_input', id_user=int(web.ctx.session.userid), attempt=text, id_problem=idp, correct=answer)
    except Exception as e:
        print e
    if answer:
        try:
            db.insert('user_problems', id_user=int(web.ctx.session.userid), id_problem=idp)
        except Exception as e:
                pass
    return answer, checks

  
      
  


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
    if 'recterms' in data:
      if 'hint' in data:
        web.ctx.session.hintlevel=min(web.ctx.session.hintlevel+1,3)
        web.ctx.session.hint=mhinter.hint(problemdata.recurrence,web.ctx.session.hintlevel)
        return render.problemtable(web.ctx.session.instance,mysolution,None,comments,False)
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
	  
      except ParserException as e:
        correct=False
        if theirsolution is not None:
          return render.problemtable(web.ctx.session.instance,mysolution,theirsolution.table,comments,correct,e.message,theircommands=data['recterms'])
        else:
          return render.problemtable(web.ctx.session.instance,mysolution,None,comments,correct,e.message,theircommands=data['recterms'])
      except (NameError,SyntaxError) as e:
        correct=False
        if theirsolution is not None:
          return render.problemtable(web.ctx.session.instance,mysolution,theirsolution.table,comments,correct,str(e),theircommands=data['recterms'])
        else:
          return render.problemtable(web.ctx.session.instance,mysolution,None,comments,correct,str(e),theircommands=data['recterms'])
      except:
          correct=False
          if theirsolution is not None:
            return render.problemtable(web.ctx.session.instance,mysolution,theirsolution.table,comments,correct,"Something went wrong",theircommands=data['recterms'])
          else:
	    return render.problemtable(web.ctx.session.instance,mysolution,None,comments,correct,"Something went wrong",theircommands=data['recterms'])
      print "received checks length" ,len(checks)
      return render.problemtable(web.ctx.session.instance,mysolution,theirsolution.table,comments,correct=correct,message=message,theircommands=data['recterms'],checks=checks)
    
    if data['action']=='new':
      constants=randomgenerator.getRandomConstants(problemdata.constants)
      web.ctx.session.instance.constants=constants
      arrays=randomgenerator.getRandomArrays(problemdata.arrays)
      web.ctx.session.instance.lists=arrays
      web.ctx.session.solutionindex=0	
      print constants
      mysolution=solutioninstance(solver2.solve(web.ctx.session.instance.lists,web.ctx.session.instance.constants,commands,web.ctx.session.instance.dimensions[0],web.ctx.session.instance.dimensions[1]))
  
      return render.problemtable(web.ctx.session.instance,mysolution,None,comments)
    elif data['action']=='showsolution':
	mysolution.show=True
	web.ctx.session.solutionindex=50
	return render.problemtable(web.ctx.session.instance,mysolution,None,comments)
    elif data['action']=='nextvalue':
	mysolution.show=True
	web.ctx.session.solutionindex+=1
	return render.problemtable(web.ctx.session.instance,mysolution,None,comments)
    elif data['action']=='comment':
      db.insert('comment', user_id=web.ctx.session.userid,problem_id=web.ctx.session.idp,comment=data['comment'])
      comments=db.query('select * from example_users eu join comment c on c.user_id=eu.id where c.problem_id='+web.ctx.session.idp)
  
      return render.problemtable(web.ctx.session.instance,mysolution,None,comments)
