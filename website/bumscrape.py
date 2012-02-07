import web
import model

render = web.templates.render('templates/')
urls = (
      '/', 'index',
      '/list', 'list',
      )

class index:
    def GET(self):
        raise web.redirect('/index.html')

class list:
    def GET(self):
       """gets active listings"""
       request = web.input(list_all=False, format='web')

       active_only = True if not request.list_all else False
       listings = model.get_listings(active_only)

       return render.listings(listings)

application = web.application(urls, globals()).wsgifunc()
