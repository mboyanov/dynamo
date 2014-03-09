import web
render = web.template.render('templates/')
class main:
  def GET(self):
    name=web.ctx.session.user
    return render.main(name)
