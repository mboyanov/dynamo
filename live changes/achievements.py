import web
import hashlib
from web import form
import config
from pdfgenerator import pdfgenerator

render = web.template.render(config.templatedir,base="layout")



class achievements:
    def GET(self):
        # do $:f.render() in the template
        
        db = web.database(dbn='mysql', db='web', user='root', pw='xaxaxa')
        data = db.query("SELECT id,type,data,title,url,description,user_id from achievements a left join user_achievements ua on a.id=ua.achievement_id AND ua.user_id="+str(web.ctx.session.userid))
        
        return render.achievements(data)
    def POST(self):
      i=web.input()
      db = web.database(dbn='mysql', db='web', user='root', pw='xaxaxa')
      data = db.query("SELECT * from achievements a where id="+str(i['achievement_id']))
      data=data[0]
      generator= pdfgenerator()
      sourceHtml=generator.generateHtml(i['person'],data['title'],data['url'])
      outputFilename = "/home/ec2-user/web.py/web.py/static/"+i['person']+data['title']+".pdf"
      generator.convertHtmlToPdf(sourceHtml,outputFilename)
      return web.seeother('/static/'+i['person']+data['title']+".pdf")     
