import web

urls = (
      '/.*', 'hello',
      )

class hello:
    def GET(self):
       return "Hello, world."

if __name__ == "__main__":
    application = web.application(urls, globals()).run()
