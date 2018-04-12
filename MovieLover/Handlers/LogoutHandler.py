from Handlers.BaseHandler import BaseHandler
class LogoutHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.clear_cookie("user")
        self.redirect('/')