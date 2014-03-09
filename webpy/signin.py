import web
import hashlib
from web import form
import config

render = web.template.render(config.templatedir,base="layout")

signin_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Password("password",  description="Password"),
    
)

class signin:
  def GET(self):
    f=signin_form();
    return render.signin(f)
   
  def POST(self):
    i=web.input()
    vars=dict(user=str(i.username))
    db = config.getDB()
    result=db.select('example_users',vars,where="user =$user")
    result=result[0]
    if hashlib.md5(i.password).hexdigest()==result['passw']:
      web.ctx.session.user=i.username
      web.ctx.session.userid=result.id;
      raise web.seeother('/collection')
    else:
      return "incorrect"
    