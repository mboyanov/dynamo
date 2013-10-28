import web
import hashlib
from web import form

render = web.template.render('templates/',base="layout")

signin_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Password("password",  description="Password"),
    
)

class compiler:
  def GET(self):
    f=signin_form();
    return 'xa'
  def POST(self):
    i=web.input()
    vars=dict(user=str(i.username))
    db = web.database(dbn='mysql', db='web', user='root', pw='')
    result=db.select('example_users',vars,where="user =$user")
    if hashlib.md5(i.password).hexdigest()==result[0]['passw']:
      web.ctx.session.user=i.username
      raise web.seeother('/collection')
    else:
      return "incorrect"
    