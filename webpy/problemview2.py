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
from commandsplitter import splitter

db = web.database(dbn='mysql', db='web', user='root', pw='xaxaxa')
render = None


def top():
    if web.ctx.session.user is None or web.ctx.session.user == '':
        raise web.seeother('/signin')


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
                db.insert('user_input', id_user=web.ctx.session.userid, attempt=text, id_problem=idp, correct=0)
                answer = False
        #if one answer is None, return false. TODO: make them separate when you get messages
        elif (mysolution.answer is not None and theirsolution.answer is None) or (
                        mysolution.answer is None and theirsolution.answer is not None):
            checks.append(["You should specify an answer with the answer keyword"])
            answer = False
        elif mysolution.answer != theirsolution.answer:
            checks.append(["Wrong answer for input:", constants, arrays, mysolution.table, mysolution.answer,
                           theirsolution.answer])
            answer = False
        elif mysolution.answer == theirsolution.answer:
            checks.append(
                ["Succeeded with input:", constants, arrays, mysolution.table, theirsolution.table, mysolution.answer,
                 theirsolution.answer])
    db.insert('user_input', id_user=web.ctx.session.userid, attempt=text, id_problem=idp, correct=1)
    try:
        db.replace('user_problems', id_user=web.ctx.session.userid, id_problem=idp)
    except:
        return answer, checks
    return answer, checks


def build(input):
    commands = []
    for i in range(6):
        command=""
        if ('left'+str(i)) in input and input['left'+str(i)]!='':
            command+=input['left'+str(i)]+'='
        if ('function'+str(i)) in input:
            command+=input['function'+str(i)]
        if ('forclause'+str(i)) in input:
            command+=' '+input['forclause'+str(i)]
        if ('whereclause'+str(i)) in input:
            command+=input['whereclause'+str(i)]
        if command.encode()!=' ':
            commands.append(command.encode())
    return commands


class problemview2:
    def GET(self):
        top()
        data = web.input()
        web.ctx.session.idp = data['idp']
        web.ctx.session.hintlevel = 0
        web.ctx.session.hint = ''
        problemdata = db.select('description', data, where='id=$idp')
        problemdata = problemdata[0]
        constants = randomgenerator.getRandomConstants(problemdata.constants)
        arrays = randomgenerator.getRandomArrays(problemdata.arrays)
        if problemdata.hints is not None:
            hinttext = 'hints=' + problemdata.hints
            exec (hinttext)
        else:
            hints = None
        if problemdata.video is not None:
            videotext = 'video=' + problemdata.video
            exec (videotext)
        else:
            video = None
        t = problem('<p>' + problemdata.description, arrays, constants, (problemdata.dimension_y, 20),
                    problemdata.solutiontext, problemdata.tableexplanation, hints, video)
        web.ctx.session.instance = t
        web.ctx.session.problemstatus = 2;
        web.ctx.session.solutionindex = 0;
        commands = re.split('[\n\r]+', problemdata.recurrence)
        comments = db.query(
            'select * from example_users eu join comment c on c.user_id=eu.id where c.problem_id=' + web.ctx.session.idp)
        mysolution = solutioninstance(
            solver2.solve(web.ctx.session.instance.lists, web.ctx.session.instance.constants, commands,
                          web.ctx.session.instance.dimensions[0], web.ctx.session.instance.dimensions[1]))
        render = web.template.render(config.templatedir, base='layout', globals={'context': web.ctx.session})
        msplitter = splitter(False)
        print commands
        builders = msplitter.split(commands)
        return render.problemtableform(web.ctx.session.instance, mysolution, None, comments, builders)


    def POST(self):
        top()

        render = web.template.render(config.templatedir, base='layout', globals={'context': web.ctx.session})
        problemdata = db.select('description', web.ctx.session, where='id=$idp')
        problemdata = problemdata[0]
        commands = re.split('[\n\r]+', problemdata.recurrence)
        comments = db.query(
            'select * from example_users eu join comment c on c.user_id=eu.id where c.problem_id=' + web.ctx.session.idp)
        mhinter = hinter()
        mysolution = solutioninstance(
            solver2.solve(web.ctx.session.instance.lists, web.ctx.session.instance.constants, commands,
                          web.ctx.session.instance.dimensions[0], web.ctx.session.instance.dimensions[1]))
        msplitter = splitter(False)
        builders = msplitter.split(commands)
        if web.ctx.session.hintlevel > 0:
            web.ctx.session.hint = mhinter.hint(problemdata.recurrence, web.ctx.session.hintlevel)
        data = web.input()

        if 'left0' in data:
            commands = build(data)
            print commands,"hello"
            message = ''
            theirsolution = None
            try:
                theirsolution = solutioninstance(
                    solver2.solve(web.ctx.session.instance.lists, web.ctx.session.instance.constants, commands,
                                  web.ctx.session.instance.dimensions[0], web.ctx.session.instance.dimensions[1]))
                print "THEIR SOLUTION:", theirsolution.table
                correct, checks = checksolution(web.ctx.session.idp, commands)
                if correct:
                    achecker = achievementchecker()
                    message = achecker.check(web.ctx.session.userid)
            except ParserException as e:
                correct = False
                if theirsolution is not None:
                    return render.problemtableform(web.ctx.session.instance, mysolution, theirsolution.table, comments,
                                               builders, correct, e.message, theircommands=commands)
                else:
                    return render.problemtableform(web.ctx.session.instance, mysolution, None, comments, builders, correct,
                                               e.message, theircommands=commands)
            except (NameError, SyntaxError) as e:
                correct = False
                if theirsolution is not None:
                    return render.problemtableform(web.ctx.session.instance, mysolution, theirsolution.table, comments,
                                               builders, correct, str(e), theircommands=commands)
                else:
                    return render.problemtableform(web.ctx.session.instance, mysolution, None, comments, builders, correct,
                                               str(e), theircommands=commands)
            except:
                correct = False
                if theirsolution is not None:
                 return render.problemtableform(web.ctx.session.instance, mysolution, theirsolution.table, comments,
                                               builders, correct, "Something went wrong",
                                               theircommands=commands)
                else:
                    return render.problemtableform(web.ctx.session.instance, mysolution, None, comments, builders, correct,
                                           "Something went wrong", theircommands=commands)
            print "received checks length", len(checks)
            return render.problemtableform(web.ctx.session.instance, mysolution, theirsolution.table, comments,
                                           builders, correct=correct, message=message, theircommands=commands,
                                           checks=checks)

        if data['action'] == 'new':
            constants = randomgenerator.getRandomConstants(problemdata.constants)
            web.ctx.session.instance.constants = constants
            arrays = randomgenerator.getRandomArrays(problemdata.arrays)
            web.ctx.session.instance.lists = arrays
            web.ctx.session.solutionindex = 0
            print constants
            mysolution = solutioninstance(
                solver2.solve(web.ctx.session.instance.lists, web.ctx.session.instance.constants, commands,
                              web.ctx.session.instance.dimensions[0], web.ctx.session.instance.dimensions[1]))

            return render.problemtableform(web.ctx.session.instance, mysolution, None, comments, builders)
        elif data['action'] == 'showsolution':
            mysolution.show = True
            web.ctx.session.solutionindex = mysolution.length
            return render.problemtable(web.ctx.session.instance, mysolution, None, comments)
        elif data['action'] == 'nextvalue':
            mysolution.show = True
            web.ctx.session.solutionindex += 1
            return render.problemtable(web.ctx.session.instance, mysolution, None, comments)
        elif data['action'] == 'comment':
            db.insert('comment', user_id=web.ctx.session.userid, problem_id=web.ctx.session.idp,
                      comment=data['comment'])
            comments = db.query(
                'select * from example_users eu join comment c on c.user_id=eu.id where c.problem_id=' + web.ctx.session.idp)

            return render.problemtable(web.ctx.session.instance, mysolution, None, comments)
