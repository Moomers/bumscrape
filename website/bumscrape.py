#!/usr/bin/env python

## fix the import path
import os, sys
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

## start the application

import web
import model

render = web.template.render('templates/')
urls = (
      '/', 'listings',
      '/about', 'about',
      )

class about:
    def GET(self):
        raise web.redirect('/about.html')

class listings:
    def GET(self):
       """gets active listings"""
       request = web.input(list_all=False, format='web')

       active_only = True if not request.list_all else False
       listings = model.get_listings(active_only)

       return render.listings(listings)

application = web.application(urls, globals()).wsgifunc()
