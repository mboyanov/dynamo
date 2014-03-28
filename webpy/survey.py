import web
import config
from top import top
from achievementchecker import achievementchecker
render = web.template.render(config.templatedir,base="layout")
db=config.getDB()

class survey:
    def GET(self):
        top()
        # do $:f.render() in the template
        return render.survey()

    def POST(self):
        top()
        data=web.input()
        if 'comment' not in data:
            data['comment']="x"
        if 'field' in data:
            query="REPLACE into survey VALUES({0},\'{1}\',{2},{3},{4},{5},{6},{7},\'{8}\')".format(web.ctx.session.userid,data['field'],data['system'],data['syntax'],data['hints'],data['commandvsmenu'],data['menuconcentration'],data['menurestrictive'],data['comment'])
            db.query(query)
            achecker=achievementchecker()
            message=achecker.awardSurvey(web.ctx.session.userid)
            return render.survey("Thank you! Survey submitted successfully! You have been awarded the Surveyor Achievement "+message)

        return render.survey("Something went wrong...Please try again")