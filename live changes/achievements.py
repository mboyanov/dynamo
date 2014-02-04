import web
import hashlib
from web import form
import config
from pdfgenerator import pdfgenerator
from time import sleep
render = web.template.render(config.templatedir,base="layout")

vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
vemail = form.regexp(r".*@.*", "must be a valid email address")

register_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Textbox("email", vemail, description="E-Mail"),
    form.Password("password", vpass, description="Password"),
    form.Password("password2", description="Repeat password"),
    validators = [
        form.Validator("Passwords did't match", lambda i: i.password == i.password2)]

)

class achievements:
    def GET(self):
        # do $:f.render() in the template
        
        db = web.database(dbn='mysql', db='web', user='root', pw='xaxaxa')
        data = db.query("SELECT * from achievements a join user_achievements ua on a.id=ua.achievement_id where ua.user_id="+str(14))
        
        return render.achievements(data)
    def POST(self):
      i=web.input()
      db = web.database(dbn='mysql', db='web', user='root', pw='xaxaxa')
      data = db.query("SELECT * from achievements a where id="+str(i['achievement_id']))
      data=data[0]
      generator= pdfgenerator()
      sourceHtml=generator.generateHtml(i['person'],data['title'],data['url'])
      outputFilename = "/home/ec2-user/web.py/web.py/static/test.pdf"
      generator.convertHtmlToPdf(sourceHtml,outputFilename)
      sleep(3)
      raise web.seeother('/static/test.pdf')
           
