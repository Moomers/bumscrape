#!/usr/bin/env python

## fix the import path
import os, sys
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

## start the application

import web
import model
import json
import csv
import StringIO

render = web.template.render('templates/')
urls = (
      '/', 'listings',
      '/about', 'about'
      )

class about:
    def GET(self):
        return render.about()

class listings:
    export_fields = ['num_tickets',
                     'price',
                     'url',
                     'title',
                     'spider',
                     'first_seen',
                     'last_seen']

    def GET(self):
       """gets active listings"""
       request = web.input(list_all=False, format='web')

       active_only = True if not request.list_all else False
       listings = model.get_listings(active_only)

       if format == 'json':
           web.header('Content-Type', 'application/json')
           return json.dumps({'listings': [
               dict((field, listing[field]) for field in self.export_fields)
               for listing in listings]})
       elif format == 'csv':
           buf = StringIO.StringIO()
           out = csv.writer(buf)
           out.writerow(self.export_fields) 
           for listing in listings:
               out.writerow([listing[field] for field in self.export_fields])
           web.header('Content-Type', 'application/csv')
           return buf.getvalue()
       else:
           return render.listings(listings)

application = web.application(urls, globals()).wsgifunc()
