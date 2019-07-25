from google.appengine.api import app_identity
from google.appengine.api import mail
import webapp2




class SendMailHandler(webapp2.RequestHandler):
    def get(self):
        mail.send_mail(sender='xxxx@google.com',
                       to="Maximus <xxxx@google.com>",
                       subject="test",
                       body="""test""")
        self.response.write("main sent")

app = webapp2.WSGIApplication([
    ('/send_mail', SendMailHandler),
], debug=True)

