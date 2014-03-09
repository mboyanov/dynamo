import web
def top():
  if web.ctx.session.user is None or web.ctx.session.user=='':
    raise web.seeother('/signin')