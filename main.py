import json
import pprint
import bottle
from bottle import Bottle, post, request, run, ServerAdapter,response
import connection
import setupDB
import scheduler
import settings
#!/usr/bin/python3

serverport = 4443
token="t7wftaseh3dz38urru89dywi8e"
certfile=""

# will need to sign this when we actually go to deploy
@post("/remindme")
def remindme_handler():
   response.set_header('MATTERMOST_TOKEN', settings.WEBHOOK_TOKEN)
   response.content_type = 'application/json'
   pprint.pprint(request.body.read())
   jsonRes = json.loads(request.body.read())
   pprint.pprint(jsonRes)

   scheduledRequest = jsonRes["text"].split(" ")
   if(scheduler.validateRequest(scheduledRequest)):
       scheduler.scheduleJob(scheduledRequest,jsonRes)
   else:
       return '{"text":"Invalid remindme request! [USAGE] !remindme NUM <seconds/minutes/hours/days>"}'

   return '{"text":"Successfully set a reminder. It will be DM\'ed to you"}'        

class SSLWSGIRefServer(ServerAdapter):
   def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        import ssl
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        srv = make_server(self.host, self.port, handler, **self.options)
        
        srv.serve_forever()
        
# conn = connection.ConnectionHandler()
srv = SSLWSGIRefServer(host="10.0.0.5", port=serverport)
run(server=srv)
