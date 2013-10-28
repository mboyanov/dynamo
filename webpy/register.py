import web
import hashlib
from web import form

render = web.template.render('templates/',base="layout") # your templates

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

class register:
    def GET(self):
        # do $:f.render() in the template
        f = register_form()
        return render.register(f)

    def POST(self):
        f = register_form()
        if not f.validates():
            return render.register(f)
        else:
	  i=web.input()
	  db = web.database(dbn='mysql', db='web', user='root', pw='')
	  n = db.insert('example_users', user=i.username,email=i.email,passw=hashlib.md5(i.password).hexdigest())
	  raise web.seeother('/signin')
            # do whatever is required for registration 
