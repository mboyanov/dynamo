import config
import randomgenerator
from problem import problem
import solver2
from solution import solutioninstance
import re
db=config.getDB()
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