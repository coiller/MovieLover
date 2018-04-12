import Settings
import tornado.escape
import pymysql
class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    @property
    def cur(self):
        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()
        return cursor
    @property
    def sql_error(self):
        return pymysql.Error

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")






