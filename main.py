import webapp2
import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class Task(db.Model):
	author = db.UserProperty()
	task = db.StringProperty(multiline=True)
	date = db.DateTimeProperty(auto_now_add=True)
	
class MainPage(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        if user:

                tasks = db.GqlQuery("SELECT * FROM Task WHERE author = :author ORDER BY date DESC LIMIT 10",
                                    author = user)

                url = users.create_logout_url(self.request.uri)
                
    
                template_values = {'user' : user, 'url': url, 'tasks' : tasks }
                path = os.path.join(os.path.dirname(__file__),'index.html')
                self.response.out.write(template.render(path, template_values))
        else:
                self.redirect(users.create_login_url(self.request.uri))
                
			
class Tasks(webapp2.RequestHandler):
	def post(self):
		task = Task()
		
		user = users.get_current_user()
		if user:
			task.author = user
			
		task.task = self.request.get('content')
		if task.task:
			task.put()
		self.redirect('/')
		
		
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/post', Tasks)
], debug=True)
