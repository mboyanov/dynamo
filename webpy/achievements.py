import web
from top import top
import config
from pdfgenerator import pdfgenerator

render = web.template.render(config.templatedir,base="layout")
db=config.getDB()


class achievements:
    def GET(self):
        top()
        data = db.query("SELECT id,type,data,title,url,description,user_id from achievements a left join user_achievements ua on a.id=ua.achievement_id AND ua.user_id="+str(web.ctx.session.userid))
        return render.achievements(data)


    def POST(self):
      top()
      i=web.input()
      data = db.query("SELECT * from achievements a where id="+str(i['achievement_id']))
      data=data[0]
      generator= pdfgenerator()
      sourceHtml=generator.generateHtml(i['person'],data['title'],data['url'])
      outputFilename = "/home/marty/web.py/webpy/test.pdf"
      generator.convertHtmlToPdf(sourceHtml,outputFilename)
      f=open(outputFilename)
      return f
           
